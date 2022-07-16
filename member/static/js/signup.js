function joinform_check(){
    var terms1 =document.getElementById("terms1");
    var terms2 =document.getElementById("terms2");
    if (!terms1.checked){
        alert("약관동의를 체크하세요!");
        terms1.focus();
        return false;
    }

    if (!terms2.checked){
        alert("약관동의를 체크하세요!");
        terms2.focus();
        return false;
    }
    
    document.join_form.submit();
}