$(document).ready(function(){ 
    S('.more-btn').click(function(){
        $(this).toggleClass('active');
        $('.nav-wrap').toggleClass('active');
    })
});