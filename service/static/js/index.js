/*********************************
 getUserMedia returns a Promise
 resolve - returns a MediaStream Object
 reject returns one of the following errors
 AbortError - generic unknown cause
 NotAllowedError (SecurityError) - user rejected permissions
 NotFoundError - missing media track
 NotReadableError - user permissions given but hardware/OS error
 OverconstrainedError - constraint video settings preventing
 TypeError - audio: false, video: false
 post_data - post data to flask api
 *********************************/
let post_address = "http://127.0.0.1:5000/receive"; // TODO 포트지정 필요
let delay = 5000;
let save_file_format = `${new Date().getTime()}.webm`;
let constraintObj = { audio: true };
var postJson;

//마이크 사용 가능한 기기 여부 확인
if (navigator.mediaDevices === undefined) {
  navigator.mediaDevices = {};
  navigator.mediaDevices.getUserMedia = function (constraintObj) {
    let getUserMedia =
      navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    if (!getUserMedia) {
      return Promise.reject(
        new Error("getUserMedia is not implemented in this browser")
      );
    }
    return new Promise(function (resolve, reject) {
      getUserMedia.call(navigator, constraintObj, resolve, reject);
    });
  };
} else {
  navigator.mediaDevices
    .enumerateDevices()
    .then((devices) => {
      devices.forEach((device) => {
        console.log(device.kind.toUpperCase(), device.label);
      });
    })
    .catch((err) => {
      console.log(err.name, err.message);
    });
}

// 마이크로 녹음
navigator.mediaDevices
  .getUserMedia(constraintObj)
  .then(function (mediaStreamObj) {
    let start = document.getElementById("recordStart");
    let mediaRecorder = new MediaRecorder(mediaStreamObj);
    let chunks = [];
    start.addEventListener("click", () => {
      mediaRecorder.start();
      console.log(mediaRecorder.state);
      setTimeout(function(){displayMessage("response", 1)}, 0);
      setTimeout(() => {
        mediaRecorder.stop();
        console.log(mediaRecorder.state);
      }, delay);
    });
    mediaRecorder.ondataavailable = function (ev) {
      chunks.push(ev.data);
    };
    mediaRecorder.onstop = () => {
      let blob = new Blob(chunks, { type: "audio/wav;" });
      postJson = post_data(blob);
      chunks = [];
    };
  })
  .catch(function (err) {
    console.log(err.name, err.message);
  });
<<<<<<< HEAD
function getCookie(name) {
  var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return value? value[2] : null;
} 
=======

//blob 데이터 post, 받은 데이터로 감정 띄우기
>>>>>>> 4c0457b10baff485f326ceb994fc1fff3f1aae8e
function post_data(blob) {
  const fd = new FormData();
  const xhr = new XMLHttpRequest();
  var result = document.getElementById("result");
  var username = getCookie('username');
  
  xhr.open("POST", post_address, false);
  fd.append("file", blob, save_file_format);
  xhr.send(fd);

  var labels = JSON.parse(xhr.responseText);
  var newDiv = document.createElement("div");
  newDiv.className = "chat-bubble";
  var newImg = document.createElement("img");
  newImg.className = "bot image";
  var newP = document.createElement("p");
  if(labels.result == "happiness"){
    newP.innerHTML = ("기쁘신가봐요")
    setTimeout(function(){displayMessage("response", 2)}, 3000);
  } else if(labels.result == "anger" ){
    newP.innerHTML = ("화가 나셨나봐요")
    setTimeout(function(){displayMessage("response", 2)}, 3000);
  } else if(labels.result == "sad"){
    newP.innerHTML = ("슬프시네요")
    setTimeout(function(){displayMessage("response", 2)}, 3000);
  } else{
    newP.innerHTML = ("다시 말씀해주세요")
  }
  newDiv.appendChild(newImg)
  newDiv.appendChild(newP);
  
  var messages = document.getElementById("chat-contents");
  messages.appendChild(newDiv);
  

  console.log(xhr.responseText);
  console.log(labels.top10[0].title);

  return labels;
}

//지정된 챗봇 답변
function displayMessage(type, number){
  var initialMessages = ["안녕하세요 니모션입니다."]
  var responseMessages = ["잠시만 기다려주세요", "현재 감정이 맞나요?", "맞으시군요, 잠시만 기다려주세요", "아니시군요 어떠한 감정이신지 화남, 기쁨, 슬픔 중에서 골라주세요", "다시 말씀해주세요"]
  
  var newDiv = document.createElement("div");
  newDiv.className = "chat-bubble";
  var newImg = document.createElement("img");
  newImg.className = "bot image";
  var newP = document.createElement("p");
  if(type == "initial") {
    newP.innerHTML = initialMessages[Math.floor(Math.random() * Math.floor(initialMessages.length))]
  } else if(number == 1){
    newP.innerHTML = responseMessages[0];
  } else if(number == 2){
    newP.innerHTML = responseMessages[1];
  } else if(number == 3){
    newP.innerHTML = responseMessages[2];
  } else if(number == 4){
    newP.innerHTML = responseMessages[3];
  } else if(number == 5){
    newP.innerHTML = responseMessages[4];
  }
  newDiv.appendChild(newImg)
  newDiv.appendChild(newP);
    
  var messages = document.getElementById("chat-contents");
  messages.appendChild(newDiv);
}

//text값 있을때 버튼 active
function arrowSubmit(){
  console.log("here")
  button = document.getElementById("submit-chat");
  text = document.getElementById("chat-message-value");
  if( text.value != ""){
    button.classList = "active";
  }else{
    button.classList.remove("active");
  }
}

//타이핑한 text값 띄우기
function submitMessage(){
  var text = document.getElementById("chat-message-value").value;
  if(text == ""){
    return
  }
  document.getElementById("chat-message-value").value = "";
  
  var newDiv = document.createElement("div");
  newDiv.className = "chat-bubble";
  var newImg = document.createElement("img");
  newImg.className = "user image";
  var newP = document.createElement("p");
  newP.innerHTML = text;
  newDiv.appendChild(newImg)
  newDiv.appendChild(newP);
  
  var messages = document.getElementById("chat-contents");
  messages.appendChild(newDiv);
  document.getElementById("submit-chat").classList.remove("active");
  if(text == "네" || text == "맞아" || text == "맞습니다" || text == "sp"){
    setTimeout(function(){displayMessage("response", 3)},1000);
    setTimeout(function(){feelingmessages(text)},1000);
  } else if(text == "아니" || text == "아니야" || text == "아닙니다" || text == "dksl"){
    setTimeout(function(){displayMessage("response", 4)},1000);
  } else if(text == "화남" || text == "화가 나요" ){
    setTimeout(function(){displayMessage("response", 1)},1000);
  } else if(text == "기쁨" || text == "아니야" || text == "아닙니다"){
    setTimeout(function(){displayMessage("response", 1)},1000);
  } else if(text == "슬픔" || text == "슬퍼" || text == "눈물"){
    setTimeout(function(){displayMessage("response", 1)},1000);
  } else{
    setTimeout(function(){displayMessage("response", 5)}, 1000);
  }
  return text;
}


//해당 감정의 영화 추천 메시지
function feelingmessages(text){
  if(text == "네" || text == "맞아" || text == "맞습니다" || text == "sp"){
    for(i=0; i<10; i++){
      var newDiv = document.createElement("div");
      newDiv.className = "chat-bubble";
      var newImg = document.createElement("img");
      newImg.className = "bot image";
      var newP = document.createElement("p");
      var messages = document.getElementById("chat-contents");
      newDiv.appendChild(newImg);
      newDiv.appendChild(newP);
      newP.innerHTML = '제목: ';
      newP.innerHTML += postJson.top10[i].title;
      newP.innerHTML += '<br/>';
      newP.innerHTML += '장르: ';
      newP.innerHTML += postJson.top10[i].genres;
      messages.appendChild(newDiv);
    }
    var newDiv = document.createElement("div");
      newDiv.className = "chat-bubble";
      var newImg = document.createElement("img");
      newImg.className = "bot image";
      var newP = document.createElement("p");
      var messages = document.getElementById("chat-contents");
      newDiv.appendChild(newImg);
      newDiv.appendChild(newP);
      newP.innerHTML = '이 영화들을 추천드려요';
      messages.appendChild(newDiv);
  }

  
}

//버튼 눌렸을때 text값 보내기
function addHandlers(){
  document.getElementById("submit-chat").addEventListener("click", submitMessage);
  document.onkeypress = function (e){
    if( e.keyCode == 13 ){
      document.getElementById("submit-chat").click();
    }
  };
  setTimeout(function(){displayMessage("initial")}, 0);
  document.getElementById("chat-message-value").addEventListener("input", arrowSubmit);
}

window.addEventListener("load", addHandlers);

