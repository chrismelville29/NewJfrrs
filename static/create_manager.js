function initialize() {
    let createButton = document.getElementById('manager_creator_button');
    createButton.onclick = onCreateButton;
}

window.onload = initialize;

function onCreateButton() {
    let username = document.getElementById('username_input').value;
    let password = document.getElementById('password_input').value;
    let errorMessage = document.getElementById('error_message');
    if(username == "" || password == "") {
        errorMessage.innerHTML = "You need a username and password.";
        return;
    }
    if (/\s/.test(username)) {
        errorMessage.innerHTML = "Username can't contain white space.";
        return;
    }

    let url = getBaseURL() + '/api/check_manager';
    let amePost = {method: 'post',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username: username,
    create: 'yes'})};

    fetch(url, amePost)

    .then((response) => response.json())

    .then(function(wasAdded) {
        if(wasAdded['status'] == 'distinct') {
            errorMessage.innerHTML = "You've successfully added '"+username+"'";
            return;
        }
        errorMessage.innerHTML = "Username '"+ username+ "' is already taken. sorry";
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
