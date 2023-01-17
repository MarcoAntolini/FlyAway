window.onload = function () {
    auth_switch();
    logged_check();
    // let title = document.getElementById("check");
    // if (title) {
    //     title.addEventListener("click", function () {
    //         let user_button = document.getElementById("user");
    //         if (user_button.classList.contains("logged")) {
    //             user_button.classList.remove("logged");
    //             user_button.innerText = "Logout";
    //         } else {
    //             user_button.classList.add("logged");
    //             user_button.innerText = "Login/Register";
    //         }
    //     });
    // };
};

function auth_switch() {
    let switch_button = document.getElementById("switch");
    if (!switch_button) return;
    switch_button.addEventListener("click", function () {
        let submit = document.getElementById("submit");
        if (switch_button.classList.contains("register")) {
            switch_button.classList.remove("register");
            switch_button.classList.add("login");
            switch_button.setAttribute("value", "Create new account");
            submit.setAttribute("value", "Login");
        } else {
            switch_button.classList.remove("login");
            switch_button.classList.add("register");
            switch_button.setAttribute("value", "Already registered?");
            submit.setAttribute("value", "Register");
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