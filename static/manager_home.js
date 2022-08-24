let username = document.getElementsByName('username')[0].content;

function initialize() {
    loadTable();

    let joinButton = document.getElementById('league_join_button');
    joinButton.onclick = onJoinButton;
}

function loadTable() {

  let url = getBaseURL() + '/api/leagues/' + username;

  fetch(url, {method: 'get'})

  .then((response) => response.json())

  .then(function(leagues) {
      document.getElementById('leagues_table').innerHTML = createTableHTML(leagues);
  })

  .catch(function(error) {
      console.log(error);
  });

}

function createTableHTML(leagues) {
    tableHTML = "<tr><th>League</th><th>Conference</th></tr>";
    for(league in leagues) {
        tableHTML+="<tr><td>"+league+"</td><td>"+leagues[league]+"</td></tr>"
    }
    return tableHTML+"<tr><td>&nbsp;</td><td></td></tr>";
}

function onJoinButton() {
    let errorMessage = document.getElementById('error_message');
    let leagueName = document.getElementById('league_name_input').value;
    let url = getBaseURL() + '/api/join_league';
    let joinLeaguePost = {method: 'post',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({manager_name: username,
    league_name: leagueName})};

    fetch(url, joinLeaguePost)

    .then((response) => response.json())

    .then(function(wasFound) {
        joinLeague(wasFound['status'], leagueName)
    })

    .catch(function(error) {
        console.log(error);
    });
}

function joinLeague(status, leagueName) {
    if(status == 'league_not_found') {
        errorMessage.innerHTML = 'League '+leagueName+' was not found.';
        return;
    }
    if(status == 'added') {
        location.reload();
    }
    errorMessage.innerHTML = "You're already in league "+leagueName+'.';

}


function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}

window.onload = initialize;
