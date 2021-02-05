// function displayLogin() {
//   let login = document.getElementById("login");
//   let register = document.getElementById("register");

//   register.style.display = "none";
//   login.style.display = "block";
// }

// function displayRegister() {
//   let login = document.getElementById("login");
//   let register = document.getElementById("register");

//   login.style.display = "none";
//   register.style.display = "block";
// }

const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});