window.onload = function () {
    auth_switch();
    logged_check();
    send_request();
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
        } else if (switch_button.classList.contains("login")) {
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

function send_request() {
    let form = document.getElementsByName("form")[0];
    if (!form) return;
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        let switch_button = document.getElementById("switch");
        let class_name = switch_button.getAttribute("class");
        let data = new FormData(this);
        data.append("class", class_name);
        fetch("/welcome", {
            method: "POST",
            body: data,
        })
            .then(function (response) {
                return response.text();
            })
            .then(function (data) {
                console.log(data);
            })
            .catch(function (error) {
                console.error(error);
            });
    });
}