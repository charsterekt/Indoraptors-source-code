var a = document.getElementById('navbar-ul');
var b = document.querySelector('.heading');
var c = document.querySelector('.heading-text');
var d = document.querySelector('.heading-button');

function showmenu() {
    a.style.visibility = "visible";
    a.style.animation = "slide 0.5s ease-in";
    b.style.visibility = "hidden";
    c.style.visibility = "hidden";
    d.style.visibility = "hidden";
}

function hidemenu(){
    a.style.visibility = "hidden";
    a.style.animation = "slide-reverse 2s ease-out";
    b.style.visibility= "visible";
    c.style.visibility= "visible";
    d.style.visibility= "visible";
}