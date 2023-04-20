function ValidateEmail(inputText){
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(inputText.value.match(mailformat)){
        return true; 
    }
    else{
        alert("Email not valid! Check your email address!");
        document.contactform.email.focus();
        return false;
    }
}

function ValidatePhoneNumber(inputText){
    var phonenumber = /^\d{5,10}$/;
    if(inputText.value.match(phonenumber)){
        return true;
    }else{
        alert("Wrong phone number. Try again! Example: 0123456789")
        return false;
    }
}