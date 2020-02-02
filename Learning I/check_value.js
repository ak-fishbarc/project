function check_value(field, p, tag_name){
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
            }else{
                display_in_p.innerHTML = field.slice(0, 1).toUpperCase() + field.slice(1) + " is valid";
                }
        }
        };
    xhttp.open("POST", "ajax_check?value=" + client_data + "&tag=" + tag_name, true);
    xhttp.send();
    }
