const scoreCardBtns = document.querySelectorAll('.score-card')
const gameDetailsWrappers = document.querySelectorAll('.game-details-wrapper')
const statBars = document.querySelectorAll('.stat-bar')
const statDiffElements = document.querySelectorAll('.stat-diff-value')
const arrows = document.querySelectorAll('.material-symbols-outlined.arrow')
const roundedLines = document.querySelectorAll('.rounded-line')
const statBtns = document.querySelectorAll('.stat-btn')
const expandBtns = document.querySelectorAll('.expand-btn')

expandBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const matchID = btn.dataset.expandId;
        const matchCard = document.querySelector(`[data-card-id="${matchID}"]`);
        const expandableDiv = matchCard.querySelector('.expandable-div')
        expandableDiv.classList.toggle('expanded')

        const matchCardScoreBtn = matchCard.querySelector('.score-card')
        matchCardScoreBtn.click()
    })
    
})

function deactivateAll() {
    statBars.forEach(el => {
        el.classList.remove('active');
    })
}

function deactivateBtns() {
    statBtns.forEach(btn => {
        btn.classList.remove('active');
    })
}

function activateStatBars(activeStatBars) {
    activeStatBars.forEach(statBar => {
        statBar.classList.add('active');
    })
}

function getTeamStatsFromBars(activeStatBars) {
    const allStats = []
    for (i = 0; i < 5; i++) {
        const currStatsBarTeam1 = activeStatBars[i].textContent;
        const currStatsBarTeam2 = activeStatBars[i+5].textContent;

        let value1;
        let value2;
        if (currStatsBarTeam1.includes("K") || currStatsBarTeam1.includes('.')) {
            value1 = parseFloat(currStatsBarTeam1.replace("K", "")) * 1000;
            value2 = parseFloat(currStatsBarTeam2.replace("K", "")) * 1000;
        } else {
            value1 = parseFloat(currStatsBarTeam1)
            value2 = parseFloat(currStatsBarTeam2)
        }
        allStats.push(value1, value2)
    }
    return allStats
}

function getStatBarWidths(activeStatBars, biggestValue) {
    const barsArray = Array.from(activeStatBars);

    return barsArray.map(statBar => {
        const text = statBar.textContent.trim().toUpperCase();
        let value;

        if (text.includes('K') || text.includes('.')) {
            value = parseFloat(text.replace("K", "")) * 1000;
        } else {
            value = parseInt(text)
        }
        const widthPct = (value / biggestValue) * 100;
        
        return { element: statBar, width: widthPct}
    })
}

function applyStatBarWidths(statWidths) {
    statWidths.forEach(({ element, width }) => {
        element.style.width = `${width}%`
    })
}

scoreCardBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        gameDetailsWrappers.forEach(el => {
            el.classList.remove('active');
        })

        arrows.forEach(el => {
            el.classList.remove('active');
        })

        deactivateBtns();

        deactivateAll();

        const matchDataId = btn.id.slice(0, -4);
        const activeGameDetailsWrapper = document.getElementById(matchDataId);
        activeGameDetailsWrapper.classList.add('active');

        scoreCardBtns.forEach(otherBtn => {
            otherBtn.classList.remove('active');
        });
        btn.classList.add('active');

        const activeArrows = activeGameDetailsWrapper.querySelectorAll('.material-symbols-outlined.arrow');
        activeArrows.forEach(arrow => {
            arrow.classList.add('active');
        })

        const activeRoundedLines = activeGameDetailsWrapper.querySelectorAll('.rounded-line');
        activeRoundedLines.forEach(el => {
            el.classList.add('active');
        })

        const activeStatDiffValuesElements = activeGameDetailsWrapper.querySelectorAll('.stat-diff-value');
        activeStatDiffValuesElements.forEach(el => {
            el.classList.add('active');
        })

        let side = activeGameDetailsWrapper.dataset.team1Side;
        let colors = []
        if (side == 'blue side') {
            colors = ['blue', 'red']
        } else {
            colors = ['red', 'blue']
        }

        gameDetailsWrappers.forEach(wrapper => {
            const dmgBtn = wrapper.querySelector('.dmg-btn');
            const goldBtn = wrapper.querySelector('.gold-btn');
            const csBtn = wrapper.querySelector('.cs-btn');

            

            function addStatLogic(btn, statClass) {
                btn.addEventListener('click', () => {
                    deactivateAll();
                    deactivateBtns()
                    btn.classList.add('active');

                    const activeStatBars = activeGameDetailsWrapper.querySelectorAll(`.stat-bar.${statClass}`);
                    const activeArrows = activeGameDetailsWrapper.querySelectorAll('.material-symbols-outlined.arrow');
                    const activeRoundedLines = activeGameDetailsWrapper.querySelectorAll('.rounded-line');
                    const activeStatDiffValuesElements = activeGameDetailsWrapper.querySelectorAll('.stat-diff-value');
                    activateStatBars(activeStatBars);

                    let side = activeGameDetailsWrapper.dataset.team1Side;
                    let colors = []
                    if (side == 'blue side') {
                        colors = ['blue', 'red']
                    } else {
                        colors = ['red', 'blue']
                    }
                       
                    idx = 1
                    activeStatBars.forEach(el => {
                        if (idx <= 5) {
                            if (side == 'blue side') {
                                el.classList.add('blue')
                            } else {
                                el.classList.add('red')
                            }
                        } else {
                            if (side == 'blue side') {
                                el.classList.add('red')
                            } else {
                                el.classList.add('blue')
                            }
                        }
                        idx += 1;
                    })

                    const allStats = getTeamStatsFromBars(activeStatBars);
                    const biggestValue = Math.max(...allStats);

                    const widths = getStatBarWidths(activeStatBars, biggestValue);
                    applyStatBarWidths(widths);

                    activeArrows.forEach(el => {el.classList.remove('hidden')});
                    activeRoundedLines.forEach(el => {el.classList.remove('red', 'blue')});

                    for (i = 0; i < 5; i++) {
                        const currStatsBarTeam1 = activeStatBars[i].textContent;
                        const currStatsBarTeam2 = activeStatBars[i+5].textContent;

                        let value1;
                        let value2;
                        if (currStatsBarTeam1.includes("K") || currStatsBarTeam1.includes('.')) {
                            value1 = parseFloat(currStatsBarTeam1.replace("K", "")) * 1000;
                            value2 = parseFloat(currStatsBarTeam2.replace("K", "")) * 1000;
                        } else {
                            value1 = parseFloat(currStatsBarTeam1)
                            value2 = parseFloat(currStatsBarTeam2)
                        }

                        let difference = Math.abs(value1 - value2)
                        if (difference >= 1000) {
                            difference = `${difference / 1000}K`
                        }
                        activeStatDiffValuesElements[i].textContent = difference;
                        
                        if (value1 > value2) {
                            activeArrows[i * 2].classList.add(colors[0])
                            activeArrows[i * 2 + 1].classList.remove(colors[0]);
                            activeArrows[i * 2 + 1].classList.add('hidden');
                            activeRoundedLines[i].classList.add(colors[0]);
                        } else {
                            activeArrows[i * 2 + 1].classList.add(colors[1])
                            activeArrows[i * 2].classList.remove(colors[1]);
                            activeArrows[i * 2].classList.add('hidden', colors[0]);
                            activeRoundedLines[i].classList.add(colors[1]);
                        }
                    }
                })
            }
            
            addStatLogic(dmgBtn, 'dmg-stat');
            addStatLogic(goldBtn, 'gold-stat');
            addStatLogic(csBtn, 'cs-stat');

            dmgBtn.click();
        })
    }) 
})

document.addEventListener("DOMContentLoaded", () => {
    

    const matchCards = document.querySelectorAll('.match-card')
    matchCards.forEach(game => {
        const allBetsWrapper = game.querySelector('.all-bets')
        const showBetsBtn = allBetsWrapper.querySelector('.show-bets-btn')
        const betsContainer = allBetsWrapper.querySelector('.bets-container');

        showBetsBtn.addEventListener('mouseenter', () => {
            betsContainer.classList.remove('hidden');
        })

        showBetsBtn.addEventListener('mouseleave', () => {
            betsContainer.classList.add('hidden');
        })

        let game_result = [0, 0]
        const matchScoreCardBtns = game.querySelectorAll('.score-card')
        matchScoreCardBtns.forEach(btn => {
            const result = btn.dataset.result;
            const resultSpan = btn.querySelector('.score')



            const colors = []
            const imgElements = btn.querySelectorAll('.team_logo')
            imgElements.forEach(img => {
                colors.push(img.dataset.color)
            })
            
            if (result == 'W–L') {
                game_result[0] += 1
                btn.style.setProperty('--after-bg', colors[0])
            } else {
                game_result[1] += 1
                btn.style.setProperty('--after-bg', colors[1])
            }

            resultSpan.textContent = `${game_result[0]} - ${game_result[1]}`

            scoreCardBtns[0].click()
        })
    })

    
})









    