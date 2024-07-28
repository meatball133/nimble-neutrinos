const hamburger = document.getElementById("hamburger");
const navItems = document.getElementById("nav-items");

hamburger.addEventListener("click", e => {
    navItems.classList.toggle("nav-items-visible");
});