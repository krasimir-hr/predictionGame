function openTab(evt, matchId, tabId) {
    let currentMatch, tabContentDivs, currentTab;

    currentMatch = document.getElementById(matchId)
    tabContentDivs = currentMatch.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContentDivs.length; i++) {
            tabContentDivs[i].style.display = 'none';
    }
    currentTab = document.getElementById(tabId)
    currentTab.style.display = 'block';
}

function expandGame(matchId, arrowId) {
    const content = document.getElementById(matchId);
    const arrow = document.getElementById(arrowId);

    const first_element = content.getElementsByClassName('tab-content')[0]


    if (first_element) {
        first_element.style.display = 'block';
    }
    content.classList.toggle('expanded')
    arrow.classList.toggle('rotate');
}