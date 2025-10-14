const burger = document.querySelector("#button");
const menu = document.querySelector(".menu");
const X = document.querySelector(".closeButton");

burger.addEventListener("click", () => {
    menu.classList.toggle("active");
})

X.addEventListener("click", () => {
    menu.classList.toggle("active");
})