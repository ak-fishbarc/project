function check_form(){
    var passcode_field = document.getElementById("passcode_check");
    var repasscode_field = document.getElementById("repasscode_check");
    var flash_message;

    var redigit = /[0-9]/;
    var reupper = /[ABCDEFGHIJKLMNOPQRSTUVWXYZ]/;
    var relower = /[abcdefghijklmnopqrstuvwxyz]/;
    var digitcheck = redigit.test(passcode_field.value);
    var uppercheck = reupper.test(passcode_field.value);
    var lowercheck = relower.test(passcode_field.value);
    var confirmcheck = false;
    var passcheck = false;
    
    if(passcode_field.value == repasscode_field.value){
        confirmcheck = true;
    }else{
        passcode_field.style.backgroundColor = "#FAEBD7";
        repasscode_field.style.backgroundColor = "#FAEBD7";
        passcode_field.style.border = "1px solid red";
        repasscode_field.style.border = "1px solid red";
        flash_message = document.getElementById("show_message_conf")
        flash_message.style.color = 'red';
        flash_message.innerHTML = "Passwords do not match!"
        return false;
    }

    if(digitcheck === true && uppercheck === true && lowercheck === true){
        passcheck = true;
    }else{
        passcode_field.style.backgroundColor = "#FAEBD7";
        repasscode_field.style.backgroundColor = "#FAEBD7";
        passcode_field.style.border = "1px solid red";
        repasscode_field.style.border = "1px solid red";
        flash_message = document.getElementById("show_message_pass")
        flash_message.style.color = 'red';
        flash_message.innerHTML = 'Password needs to contain one digit, uppercase letter and lowercase letter!'
        }
    
    if(passcheck === true && confirmcheck === true){
    document.getElementById("register_form").submit();
        return true;
    }
}
