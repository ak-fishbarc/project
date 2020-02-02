function display_message(error_code){
    var display_in_p = document.getElementById("display_error_msg");
    var error_code = error_code;
    if(error_code=='registration'){
        display_in_p.innerHTML = "Something went wrong with registration. Please try again.";
    }else if(error_code=='authentication'){
        display_in_p.innerHTML = "User was not identified. Please log in.";
    }else if(error_code=='request'){
        display_in_p.innerHTML = "Something went wrong. Please try again.";
    }
}