window.onload = function () {
    auth_switch();
    logged_check();
};

function auth_switch() {
    let switch_button = document.getElementById("switch");
    if (!switch_button) return;
    switch_button.addEventListener("click", function () {
        let submit = document.getElementById("submit");
        if (!submit) return;
        let type = document.getElementById("submit_type");
        if (!type) return;
        if (switch_button.classList.contains("register")) {
            switch_button.setAttribute("value", "Create new account");
            switch_button.classList.remove("register");
            switch_button.classList.add("login");
            submit.setAttribute("value", "Login");
            type.setAttribute("value", "login");
        } else if (switch_button.classList.contains("login")) {
            switch_button.setAttribute("value", "Already registered?");
            switch_button.classList.remove("login");
            switch_button.classList.add("register");
            submit.setAttribute("value", "Register");
            type.setAttribute("value", "register");
        }
    });
}


function logged_check() {
    let user_button = document.getElementById("user");
    if (!user_button) return;
    user_button.addEventListener("DOMAttrModified", function (event) {
        if (event.attrName !== "class") return;
        if (user_button.classList.contains("logged")) {
            user_button.innerText = "Logout";
            user_button.setAttribute("href", "/logout");
        } else {
            user_button.innerText = "Login/Register";
            user_button.setAttribute("href", "/welcome");
        }
    });
}