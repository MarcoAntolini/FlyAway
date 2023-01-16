window.onload = function () {
    let button = document.getElementById("switch");
    button.addEventListener("click", function () {
        let submit = document.getElementById("submit");
        if (button.classList.contains("register")) {
            button.classList.remove("register");
            button.classList.add("login");
            button.setAttribute("value", "Create new account");
            submit.setAttribute("value", "Login");
        } else {
            button.classList.remove("login");
            button.classList.add("register");
            button.setAttribute("value", "Already registered?");
            submit.setAttribute("value", "Register");
        }
    });
};