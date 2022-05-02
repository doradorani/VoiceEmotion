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

function displayMessage(type){
  var initialMessages = ["안녕하세요 니모션입니다."]
  var responseMessages = ["영화를 추천해드릴게요"]
  
  var newDiv = document.createElement("div");
  newDiv.className = "chat-bubble";
  var newImg = document.createElement("img");
  newImg.className = "bot image";
  var newP = document.createElement("p");
  newP.innerHTML =  type == "initial" ? initialMessages[Math.floor(Math.random() * Math.floor(initialMessages.length))] : responseMessages[Math.floor(Math.random() * Math.floor(responseMessages.length))];
  newDiv.appendChild(newImg)
  newDiv.appendChild(newP);
  
  
  var messages = document.getElementById("chat-contents");
  messages.appendChild(newDiv);
}

function arrowSubmit(){
  console.log("here")
  text = document.getElementById("chat-message-value");
  if( label.value == " "){
    button.classList = "active";
  }else{
    button.classList.remove("active");
  }
}

function addHandlers(){
  setTimeout(function(){displayMessage("initial")}, 1500);
  document.getElementById("chat-message-value").addEventListener("input", arrowSubmit);
}

window.addEventListener("load", addHandlers);

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

navigator.mediaDevices
  .getUserMedia(constraintObj)
  .then(function (mediaStreamObj) {
    let start = document.getElementById("recordStart");
    let mediaRecorder = new MediaRecorder(mediaStreamObj);
    let chunks = [];

    start.addEventListener("click", () => {
      mediaRecorder.start();
      console.log(mediaRecorder.state);
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
      post_data(blob);
      chunks = [];
    };
  })
  .catch(function (err) {
    console.log(err.name, err.message);
  });

function post_data(blob) {
  const fd = new FormData();
  const xhr = new XMLHttpRequest();
  var result = document.getElementById("result");

  xhr.open("POST", post_address, false);
  fd.append("file", blob, save_file_format);
  xhr.send(fd);

  var label = JSON.parse(xhr.responseText);
  var newDiv = document.createElement("div");
  newDiv.className = "chat-bubble";
  var newImg = document.createElement("img");
  newImg.className = "user image";
  var newP = document.createElement("p");
  if(label.result == "happiness"){
    newP.innerHTML = ("기쁘신가봐요")
  } else if(label.result == "anger" ){
    newP.innerHTML = ("화가 나셨나봐요")
  } else if(label.result == "angry"){
    newP.innerHTML = ("화가 나셨나봐요")
  } else if(label.result == "disgust"){
    newP.innerHTML = ("역겨우시네요")
  } else if(label.result == "fear"){
    newP.innerHTML = ("무서우신가봐요")
  } else if(label.result == "neutral"){
    newP.innerHTML = ("평범한 상태시군요")
  } else if(label.result == "sad"){
    newP.innerHTML = ("슬프시네요")
  } else if(label.result == "surprise"){
    newP.innerHTML = ("놀라셨네요")
  } else{
    newP.innerHTML = ("다시 말씀해주세요")
  }
  newDiv.appendChild(newImg);
  newDiv.appendChild(newP);
  
  var messages = document.getElementById("chat-contents");
  messages.appendChild(newDiv);
  setTimeout(function(){displayMessage("response")}, 3000);

  console.log(xhr.responseText);

  // result.innerHTML += label.top10;
}

function submitMessage(){  
  var newDiv = document.createElement("div");
  newDiv.className = "chat-bubble";
  var newImg = document.createElement("img");
  newImg.className = "user image";
  var newP = document.createElement("p");
  if(label.result == "happiness"){
    newP.innerHTML = ("기쁘신가봐요")
  } else if(label.result == "anger" ){
    newP.innerHTML = ("화가 나셨나봐요")
  } else if(label.result == "angry"){
    newP.innerHTML = ("화가 나셨나봐요")
  } else if(label.result == "disgust"){
    newP.innerHTML = ("역겨우시네요")
  } else if(label.result == "fear"){
    newP.innerHTML = ("무서우신가봐요")
  } else if(label.result == "neutral"){
    newP.innerHTML = ("평범한 상태시군요")
  } else if(label.result == "sad"){
    newP.innerHTML = ("슬프시네요")
  } else if(label.result == "surprise"){
    newP.innerHTML = ("놀라셨네요")
  } else{
    newP.innerHTML = ("다시 말씀해주세요")
  }
  newDiv.appendChild(newImg);
  newDiv.appendChild(newP);
  
  var messages = document.getElementById("chat-contents");
  messages.appendChild(newDiv);
  setTimeout(function(){displayMessage("response")}, 3000);

}