$(document).ready(function(){ 
    $('.more-btn').click(function(){
        $(this).toggleClass('active');
        $('.nav-wrap').toggleClass('active');
        $('.gnb').toggleClass('on');
        $('.login').toggleClass('on');
    });

});

// $(document).ready(function() {
//     $('.more-btn').click(function() {
//         $(this).addClass('active');
//     });
// });

// function active() {
//     document.getElementById('gnb').style.display = 'block';
//     document.getElementById('login').style.display = 'block';
//     document.getElementById('btn').classList.add('active');
// }