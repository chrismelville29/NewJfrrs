function initialize() {
    document.getElementById('conference_selector').innerHTML = getConferenceSelectorHTML();

    let conferenceButton = document.getElementById('conference_selector_button');
    conferenceButton.onclick = onConferenceSelectorButton;
}


function getConferenceSelectorHTML() {
    return "<option value='m'>Men's MIAC</option><option value='f'>Women's MIAC</option>";
}

function onConferenceSelectorButton() {
    let userChoice = document.getElementById('conference_selector').value;
    let link = getBaseURL() + '/athletes/1408_'+userChoice;
    window.location.assign(link);
}


function getBaseURL() {
    return window.location.protocol+'//'+window.location.hostname+':'+window.location.port;
}
window.onload = initialize;
