let username = document.getElementsByName('username')[0].content;

function initialize() {
    loadTable();
    createLeagueLink();

    let joinButton = document.getElementById('league_join_button');
    joinButton.onclick = onJoinButton;
}

function loadTable() {

  let url = getBaseURL() + '/api/managers/' + username;

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
    let tableHTML = "<tr><th>League</th><th>Conference</th></tr>";
    for(league in leagues) {
        let linkTag = "<a href ='/league_home/"+league+"/"+username+"'>"+league.replaceAll("_"," ")+"</a>";
        tableHTML+="<tr><td>"+linkTag+"</td><td>"+leagues[league]+"</td></tr>"
    }
    return tableHTML+"<tr><td>&nbsp;</td><td></td></tr>";
}

function onJoinButton() {
    let leagueName = document.getElementById('join_league_name_input').value.replaceAll(" ","_");
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
    let errorMessage = document.getElementById('error_message');
    if(status == 'league_not_found') {
        errorMessage.innerHTML = 'League '+leagueName+' was not found.';
        return;
    }
    if(status == 'added') {
        location.reload();
    }
    errorMessage.innerHTML = "You're already in league "+leagueName+'.';

}

function createLeagueLink() {
    let createLink = document.getElementById('create_league_link');
    createLink.innerHTML = "<a href = '/create_league/"+username+"'>Create League</a>";
}



function getBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port;
    return baseURL;
}

window.onload = initialize;
