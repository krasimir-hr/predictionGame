const predictCards = document.querySelectorAll('.match-card.predict');

predictCards.forEach(card => {
   const predictTeamBtns = card.querySelectorAll('.predict-team');
   const predictScoreBtns = card.querySelectorAll('.predict-score');

   const predictTeam1Btn = predictTeamBtns[0];
   const predictTeam2Btn = predictTeamBtns[1];

   predictTeam1Btn.addEventListener('click', () => {
      predictTeam1Btn.classList.remove('not-selected')
      predictTeam1Btn.classList.add('selected')

      predictTeam2Btn.classList.remove('selected')
      predictTeam2Btn.classList.add('not-selected')

      let idx = 0;
      predictScoreBtns.forEach(btn => {
         removeAllSelectedScores(predictScoreBtns);
         btn.textContent = `3-${idx}`;
         idx++;
      })
   })

   predictTeam2Btn.addEventListener('click', () => {
      predictTeam2Btn.classList.remove('not-selected')
      predictTeam2Btn.classList.add('selected')

      predictTeam1Btn.classList.remove('selected')
      predictTeam1Btn.classList.add('not-selected')

      let idx = 0;
      predictScoreBtns.forEach(btn => {
         removeAllSelectedScores(predictScoreBtns);
         btn.textContent = `${idx}-3`;
         idx++;
      })
   })

   predictScoreBtns.forEach(btn => {
      btn.addEventListener('click', () => {
         removeAllSelectedScores(predictScoreBtns);
         addNotSelectedScores(predictScoreBtns);
         btn.classList.remove('not-selected');
         btn.classList.add('selected');

         const scoreList = gatherBetInfo(card);
         const team1Score = scoreList[0];
         const team2Score = scoreList[1];
         const matchId = card.dataset.predictId;

         const predictStatusEls = card.querySelectorAll('.predict-status');
         predictStatusEls[0].classList.add('hidden');
         predictStatusEls[2].classList.add('hidden');
         predictStatusEls[1].classList.remove('hidden')
         
         fetch('/submit-bet/', {
            method: 'POST',
            header: {
               'Content-Type': 'application/json',
               'x-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
               match_id: matchId,
               team1_score: team1Score,
               team2_score: team2Score
            })
         })
         .then(response => response.json())
         .then(data => {
            return new Promise(resolve => {
               setTimeout(() => resolve(data), 500);
            })
         })
         .then(data => {
            if (data.success) {
               predictStatusEls[1].classList.add('hidden');
               predictStatusEls[2].classList.remove('hidden');
            } else {
               alert('Error: ' + data.error);
            }
         })
      })
   })
})


function removeAllSelectedScores(btns) {
   btns.forEach(btn => {
      btn.classList.remove('selected');
      btn.classList.remove('not-selected');
   })
}

function addNotSelectedScores(btns) {
   btns.forEach(btn => {
      btn.classList.add('not-selected');
   })
}

function gatherBetInfo(card) {
   const score = card.querySelector('.predict-score.selected').textContent;
   return score.split('-').map(Number);
}

function getCookie(name) {
   let cookieValue = null;
   if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
         const cookie = cookies[i].trim();
         if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
         }
      }
   }
   return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
   predictCards.forEach(card => {
      const matchId = card.dataset.predictId;
      const matchDate = card.dataset.matchDate;

      const lockTime = parseCustomDate(matchDate);
      const now = new Date();

      let matchLocked = false;

      if (lockTime && now >= lockTime) {
         matchLocked = true;
         const predictTeamBtns = card.querySelectorAll('.predict-team');
         const predictScoreBtns = card.querySelectorAll('.predict-score');
         const predictStatusEls = card.querySelectorAll('.predict-status');
         predictStatusEls[0].classList.add('hidden');
         predictStatusEls[1].classList.add('hidden');
         predictStatusEls[2].classList.add('hidden');
         predictStatusEls[3].classList.remove('hidden');
            predictTeamBtns.forEach(btn => {
               btn.classList.add('locked');
            })

            predictScoreBtns.forEach(btn => {
               btn.classList.add('locked');
            })
         }
      
      if (userBets && userBets[matchId]) {
         const { team1_score, team2_score } = userBets[matchId];

         const predictTeamBtns = card.querySelectorAll('.predict-team');
         const predictScoreBtns = card.querySelectorAll('.predict-score');

         const predictStatusEls = card.querySelectorAll('.predict-status');
         predictStatusEls[0].classList.add('hidden');
         predictStatusEls[1].classList.add('hidden');
         predictStatusEls[2].classList.remove('hidden');
         if (matchLocked) {
            predictStatusEls[2].classList.add('hidden');
            predictStatusEls[3].classList.remove('hidden');
         }

         if (team1_score === 3) {
            predictTeamBtns[0].classList.add('selected');
            predictTeamBtns[1].classList.add('not-selected');
            let idx = 0;
            predictScoreBtns.forEach(btn => {
               removeAllSelectedScores(predictScoreBtns);
               btn.textContent = `3-${idx}`;
               idx++;
            })
         } else if (team2_score === 3) {
            predictTeamBtns[1].classList.add('selected');
            predictTeamBtns[0].classList.add('not-selected');
            let idx = 0;
            predictScoreBtns.forEach(btn => {
               removeAllSelectedScores(predictScoreBtns);
               btn.textContent = `${idx}-3`;
               idx++;
            })
         }

         predictScoreBtns.forEach(btn => {
            if (btn.textContent === `${team1_score}-${team2_score}`) {
                  btn.classList.add('selected');
                  btn.classList.remove('not-selected');
            } else {
                  btn.classList.remove('selected');
                  btn.classList.add('not-selected');
            }
         });
      }
   })
})

function parseCustomDate(str) {
  const parts = str.split(',').map(s => s.trim());

  if (parts.length !== 3) {
    console.error("Date format not recognized.");
    return null;
  }

  const [monthDay, year, timeWithMeridian] = parts;

  let [time, meridian] = timeWithMeridian.split(' ');
  let [hour, minute] = time.split(':');

  if (!minute) minute = "00";

  hour = parseInt(hour, 10);
  if (meridian.toLowerCase() === "p.m." && hour !== 12) hour += 12;
  if (meridian.toLowerCase() === "a.m." && hour === 12) hour = 0;

  const dateString = `${monthDay}, ${year} ${hour.toString().padStart(2, '0')}:${minute}`;

  return new Date(dateString);
}