function initialize() {
    let loginButton = document.getElementById('login_button');
    loginButton.onclick = onLoginButton;
}

window.onload = initialize;

function onLoginButton() {
    let username = document.getElementById('username_input').value;
    let password = document.getElementById('password_input').value;
    let errorMessage = document.getElementById('error_message');
    if(password == "") {
        errorMessage.innerHTML = "You need a password.";
        return;
    }

    let url = getBaseURL() + '/api/check_manager';
    let namePost = {method: 'post',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username: username,
    create: 'no'})};

    fetch(url, namePost)

    .then((response) => response.json())

    .then(function(wasFound) {
        if(wasFound['status'] == 'found') {
            let link = getBaseURL() + '/manager_home/'+username;
            window.location.assign(link);
        }
        errorMessage.innerHTML = "Username "+ username+ " doesn't match with anything. sorry";
    })

    .catch(function(error) {
        console.log(error);
    });


}

function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}
