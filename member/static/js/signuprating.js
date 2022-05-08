// var user_id


// document.addEventListener("DOMContentLoaded", function(){
//     var user_id = getCookie('user_id');
//     var image = JSON.parse("{{ movieJson|escapejs }}");
    
//     for(i=0;i<20;i++){
//         var newDiv = document.createElement("div");
//         newDiv.className = "poster-rating";
//         var newImg = document.createElement("img");
//         newImg.className = "poster";
//         var newH5 = document.createElement("h5");
//         newH5.className = "title";
//         var newSelect = document.createElement("select");
//         newSelect.classname= "select";
//         var newOption1 = document.createElement("option");
//         newOption1.classname= "stars";
//         var newOption2 = document.createElement("option");
//         newOption2.classname= "stars";
//         var newOption3 = document.createElement("option");
//         newOption3.classname= "stars";
//         var newOption4 = document.createElement("option");
//         newOption4.classname= "stars";
//         var newOption5 = document.createElement("option");
//         newOption5.classname= "stars";

//         newDiv.appendChild(newImg)
//         newDiv.appendChild(newSelect)
//         newSelect.appendChild(newOption1)
//         newSelect.appendChild(newOption2)
//         newSelect.appendChild(newOption3)
//         newSelect.appendChild(newOption4)
//         newSelect.appendChild(newOption5);

//         newImg.src = image.image;
//         newSelect.name = "rating"
//         newOption1.value = 1;
//         newOption1.innerHTML = "★☆☆☆☆";
//         newOption2.value = 2;
//         newOption2.innerHTML = "★★☆☆☆";
//         newOption3.value = 3;
//         newOption3.innerHTML = "★★★☆☆";
//         newOption4.value = 4;
//         newOption4.innerHTML = "★★★★☆";
//         newOption5.value = 5;
//         newOption5.innerHTML = "★★★★★";
              
//         var ratings = document.getElementById("ratings");
//         ratings.appendChild(newDiv);
//     }

//     return user_id
// });

