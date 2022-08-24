function initialize() {
    document.getElementById('conference_selector').innerHTML = getConferenceSelectorHTML();

    let createButton = document.getElementById('league_creator_button');
    createButton.onclick = onCreateButton;
}

window.onload = initialize;


function getConferenceSelectorHTML() {
    return "<option value='1408_m'>Men's MIAC</option><option value='1408_f'>Women's MIAC</option>";
}


function onCreateButton() {
    let leagueName = document.getElementById('league_name_input').value;
    let conference = document.getElementById('conference_selector').value;
    let errorMessage = document.getElementById('error_message');
    if(leagueName == "") {
        errorMessage.innerHTML = "Your league needs a name";
        return;
    }


    let url = getBaseURL() + '/api/create_league';

    let amePost = {method: 'post',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name: leagueName,
    conference: conference})};

    fetch(url, amePost)

    .then((response) => response.json())

    .then(function(wasAdded) {
        if(wasAdded['status'] == 'distinct') {
            errorMessage.innerHTML = "You've successfully added league'"+leagueName+"'";
            return;
        }
        errorMessage.innerHTML = "Username '"+ leagueName+ "' is already taken. sorry";
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
