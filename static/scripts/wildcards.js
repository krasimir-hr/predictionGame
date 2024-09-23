championSearchURL = '/search-champions/?q=';
playerSearchURL = '/search-players/?q=';
teamSearchURL = '/search-teams/?q=';


function setupSearch(inputId, suggestionListId, url) {
    const suggestionList = document.getElementById(suggestionListId)
    suggestionList.style.display = 'none'

    document.getElementById(inputId).addEventListener('input', function() {
        const query = this.value

        if (query.length > 0) {
            fetch(url + query)
                .then(response => {
                    console.log('Response Status:', response.status)
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.json()
                })
                .then(data => {
                    console.log('Fetched data:', data)
                    suggestionList.innerHTML = '';

                    data.forEach(result => {
                        const li = document.createElement('li');
                        li.textContent = result.name
                        li.onclick = function() {
                            document.getElementById(inputId).value = result.name;
                            suggestionList.innerHTML = '';
                        };
                        suggestionList.appendChild(li);

                    });
                    suggestionList.style.display = 'block';
                });
        } else {
            suggestionList.innerHTML = '';
        }
    });

    document.getElementById(inputId).addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && suggestionList.children.length > 0) {
            event.preventDefault();
            const firstSuggestion = suggestionList.children[0];
            document.getElementById(inputId).value = firstSuggestion.textContent;
            suggestionList.innerHTML = '';
            suggestionList.style.display = 'none';
        }
    });

    document.addEventListener('click', function(event) {
        const target = event.target;
        if (!document.getElementById(inputId).contains(target) && !suggestionList.contains(target)) {
            suggestionList.innerHTML = '';
            suggestionList.style.display = 'none';
        }
    });
}


document.addEventListener('DOMContentLoaded', function() {
    setupSearch('id_most_picked_top', 'most-picked-top-champion-list', championSearchURL);
    setupSearch('id_most_picked_jgl', 'most-picked-jgl-champion-list', championSearchURL);
    setupSearch('id_most_picked_mid', 'most-picked-mid-champion-list', championSearchURL);
    setupSearch('id_most_picked_bot', 'most-picked-bot-champion-list', championSearchURL);
    setupSearch('id_most_picked_sup', 'most-picked-sup-champion-list', championSearchURL);
    setupSearch('id_most_banned_champion', 'most-banned-champion-list', championSearchURL);
    setupSearch('id_player_with_most_kills', 'most-kills-list', playerSearchURL);
    setupSearch('id_player_with_most_assists', 'most-assists-list', playerSearchURL);
    setupSearch('id_player_with_most_deaths', 'most-deaths-list', playerSearchURL);
    setupSearch('id_tournament_winner', 'teams-list', teamSearchURL);
})

