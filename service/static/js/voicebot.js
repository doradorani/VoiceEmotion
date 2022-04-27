var accessToken = "df3c39f0c9c94fcfb913332577f33d90",
baseUrl = "https://api.api.ai/v1/",
$speechInput,
$recBtn,
recognition,
messageRecording = "잠시만 기다려주세요",
messageCouldntHear = "잘 못 들었어요. 다시 말씀해주시겠어요?",
messageInternalError = " 서버에 문제가 있는것 같아요",
messageSorry = "죄송해요 대답해드리기 어려워요";

$(document).ready(function() {
$speechInput = $("#speech");
$recBtn = $("#rec");

$speechInput.keypress(function(event) {
  if (event.which == 13) {
    event.preventDefault();
    send();
  }
});
$recBtn.on("click", function(event) {
  switchRecognition();
});
$(".debug__btn").on("click", function() {
  $(this).next().toggleClass("is-active");
  return false;
});
});

function startRecognition() {
recognition = new webkitSpeechRecognition();
recognition.continuous = false;
    recognition.interimResults = false;

recognition.onstart = function(event) {
  respond(messageRecording);
  updateRec();
};
recognition.onresult = function(event) {
  recognition.onend = null;
  
  var text = "";
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      text += event.results[i][0].transcript;
    }
    setInput(text);
  stopRecognition();
};
recognition.onend = function() {
  respond(messageCouldntHear);
  stopRecognition();
};
recognition.lang = "en-US";
recognition.start();
}

function stopRecognition() {
if (recognition) {
  recognition.stop();
  recognition = null;
}
updateRec();
}

function switchRecognition() {
if (recognition) {
  stopRecognition();
} else {
  startRecognition();
}
}

function setInput(text) {
$speechInput.val(text);
send();
}

function updateRec() {
$recBtn.text(recognition ? "Stop" : "Speak");
}

function send() {
var text = $speechInput.val();
$.ajax({
  type: "POST",
  url: baseUrl + "query",
  contentType: "application/json; charset=utf-8",
  dataType: "json",
  headers: {
    "Authorization": "Bearer " + accessToken
  },
  data: JSON.stringify({query: text, lang: "en", sessionId: "yaydevdiner"}),

  success: function(data) {
    prepareResponse(data);
  },
  error: function() {
    respond(messageInternalError);
  }
});
}

function prepareResponse(val) {
var debugJSON = JSON.stringify(val, undefined, 2),
  spokenResponse = val.result.speech;
  //spokenResponse = " I am not yet able to answer this, but my master will train me very soon! stay tuned!"
respond(spokenResponse);
debugRespond(debugJSON);
}

function debugRespond(val) {
$("#response").text(val);
}

function respond(val) {
if (val == "") {
  val = messageSorry;
}

if (val !== messageRecording) {
  var msg = new SpeechSynthesisUtterance();
  msg.voiceURI = "native";
  msg.text = val;
  msg.lang = "en-US";
  window.speechSynthesis.speak(msg);
}

$("#spokenResponse").addClass("is-active").find(".spoken-response__text").html(val);
}