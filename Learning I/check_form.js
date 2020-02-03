var keys = [];
function check_value(field, p, tag_name){
    var clear_key = keys.lastIndexOf(field);
    var check_field = document.getElementById(field);
    var display_in_p = document.getElementById(p);
    var client_data = check_field.value;
    var server_data;
    var tag_name = tag_name;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            server_data = this.responseText;
            if(server_data == 'One'){
                display_in_p.innerHTML = field.slice(0, 1).toUpperCase() + field.slice(1) + " is already taken.";
                document.getElementById(field).style.backgroundColor = "#FAEBD7";
                keys[clear_key] = 'undefined';
                console.log(keys)
            }else{
                display_in_p.innerHTML = field.slice(0, 1).toUpperCase() + field.slice(1) + " is valid";
                if(keys[clear_key] != field){
                    if(keys.includes('undefined')){
                        keys[keys.lastIndexOf('undefined')] = field;
                    }else{
                        keys.push(field);
                        console.log(keys)
                    }
                }else{
                    keys[clear_key] = field;
                    console.log(keys)
                }
                }
        }
        };
    xhttp.open("POST", "ajax_check?value=" + client_data + "&tag=" + tag_name, true);
    xhttp.send();
    }

function check_form(){
    var flash_message;

    var passcode_field = document.getElementById("passcode_check");
    var repasscode_field = document.getElementById("repasscode_check");

    var redigit = /[0-9]/;
    var reupper = /[ABCDEFGHIJKLMNOPQRSTUVWXYZ]/;
    var relower = /[abcdefghijklmnopqrstuvwxyz]/;
    var digitcheck = redigit.test(passcode_field.value);
    var uppercheck = reupper.test(passcode_field.value);
    var lowercheck = relower.test(passcode_field.value);
    var confirmcheck = false;
    var passcheck = false;

    if(passcode_field.value == repasscode_field.value){
        flash_message = document.getElementById("show_message_conf");
        flash_message.innerHTML = "";
        confirmcheck = true;
    }else{
        passcode_field.style.backgroundColor = "#FAEBD7";
        repasscode_field.style.backgroundColor = "#FAEBD7";
        passcode_field.style.border = "1px solid red";
        repasscode_field.style.border = "1px solid red";
        flash_message = document.getElementById("show_message_conf");
        flash_message.style.color = 'red';
        flash_message.innerHTML = "Passwords do not match!";
    }

    if(digitcheck === true && uppercheck === true && lowercheck === true){
        flash_message = document.getElementById("show_message_pass");
        flash_message.innerHTML = "";
        passcheck = true;
    }else{
        passcode_field.style.backgroundColor = "#FAEBD7";
        repasscode_field.style.backgroundColor = "#FAEBD7";
        passcode_field.style.border = "1px solid red";
        repasscode_field.style.border = "1px solid red";
        flash_message = document.getElementById("show_message_pass");
        flash_message.style.color = 'red';
        flash_message.innerHTML = 'Password needs to contain one digit, uppercase letter and lowercase letter!';
        }

    if(passcheck === true && confirmcheck === true && keys.includes('email') && keys.includes('name')){
        keys = [];
        document.getElementById("register_form").submit();
        return true;
    }
}
