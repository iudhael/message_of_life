

/*navbar*/

var roundedLogin = document.querySelector(".rounded-login");

var roundedSigin = document.querySelector(".rounded-sigin");

if (roundedLogin.classList.contains("rounded-login") && roundedLogin.classList.contains("active")) {
    roundedLogin.style.border = "2px #FE451E solid";
    roundedLogin.style.textDecoration = "none";

}
else {
    //roundedLogin.style.border = "2px white solid";
    
}

if (roundedSigin.classList.contains("rounded-sigin") && roundedSigin.classList.contains("active")) {
    roundedSigin.style.border = "2px #FE451E solid";
    roundedSigin.style.textDecoration = "none";
    
} 
else {
    
    //roundedSigin.style.backgroundColor = "#FE451E";
}


/*end navbar*/

/*login*/
//show-hide password login
function password_show_hide() {
    var x = document.getElementById("password");
    var show_eye = document.getElementById("show_eye");
    var hide_eye = document.getElementById("hide_eye");
    hide_eye.classList.remove("d-none");
    if (x.type === "password") {
      x.type = "text";
      show_eye.style.display = "none";
      hide_eye.style.display = "block";
    } else {
      x.type = "password";
      show_eye.style.display = "block";
      hide_eye.style.display = "none";
    }
  }


/*end login*/





