let leagueName = document.getElementsByName('league_name')[0].content;
let username = document.getElementsByName('username')[0].content;

function initialize() {
    loadManagerSelector();

    makeWelcomeMessage();


    let managersButton = document.getElementById('manager_selector_button');
    managersButton.onclick = onManagerSelectorButton;
}

function loadManagerSelector() {

  let url = getBaseURL() + '/api/leagues/' + leagueName;

  fetch(url, {method: 'get'})

  .then((response) => response.json())

  .then(function(league) {
      document.getElementById('managers_selector').innerHTML = getManagerSelectorHTML(league['managers']);
  })

  .catch(function(error) {
      console.log(error);
  });

}


function getManagerSelectorHTML(managers) {
    let selectorHTML = "";
    for(manager in managers) {
        selectorHTML += "<option value = '" + managers[manager] + "'>" + managers[manager] + "</option>";
    }
    return selectorHTML;
}

function onManagerSelectorButton() {

}

function makeWelcomeMessage() {
    let message = "Welcome to league "+leagueName.replaceAll("_", " ")+", "+username;
    document.getElementById('welcome_message').innerHTML = message;
}


function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}

window.onload = initialize;
