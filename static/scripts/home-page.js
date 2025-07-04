// DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  const statBtns = document.querySelectorAll(".stat-btn");
  const scoreCardBtns = document.querySelectorAll(".score-card");
  const expandBtns = document.querySelectorAll(".expand-btn");
  const matchCards = document.querySelectorAll(".match-card");
  const gameDetailsWrappers = document.querySelectorAll(".game-details-wrapper");

  // Expand buttons
  expandBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const matchID = btn.dataset.expandId;
      const matchCard = document.querySelector(`[data-card-id="${matchID}"]`);
      const expandableDiv = matchCard.querySelector(".expandable-div");
      expandableDiv.classList.toggle("expanded");

      const matchCardScoreBtn = matchCard.querySelector(".score-card");
      matchCardScoreBtn.click();
    });
  });

  // Score card click
  scoreCardBtns.forEach((btn) => {
    btn.addEventListener("click", () => handleScoreCardClick(btn));
  });

  // Attach stat button handlers ONCE
  document.querySelectorAll(".dmg-btn").forEach((btn) => {
    btn.addEventListener("click", () => handleStatClick(btn, "dmg-stat"));
  });
  document.querySelectorAll(".gold-btn").forEach((btn) => {
    btn.addEventListener("click", () => handleStatClick(btn, "gold-stat"));
  });
  document.querySelectorAll(".cs-btn").forEach((btn) => {
    btn.addEventListener("click", () => handleStatClick(btn, "cs-stat"));
  });

  // Hover show bets
  matchCards.forEach((game) => {
    const allBetsWrapper = game.querySelector(".all-bets");
    const showBetsBtn = allBetsWrapper.querySelector(".show-bets-btn");
    const betsContainer = allBetsWrapper.querySelector(".bets-container");

    showBetsBtn.addEventListener("mouseenter", () => {
      betsContainer.classList.remove("hidden");
    });
    showBetsBtn.addEventListener("mouseleave", () => {
      betsContainer.classList.add("hidden");
    });
  });

  // Initialize match results
  matchCards.forEach((game) => {
    const matchScoreCardBtns = game.querySelectorAll(".score-card");
    let game_result = [0, 0];

    matchScoreCardBtns.forEach((btn) => {
      const result = btn.dataset.result;
      const resultSpan = btn.querySelector(".score");
      const colors = Array.from(btn.querySelectorAll(".team_logo")).map((img) => img.dataset.color);

      if (result === "W–L") {
        game_result[0]++;
        btn.style.setProperty("--after-bg", colors[0]);
      } else {
        game_result[1]++;
        btn.style.setProperty("--after-bg", colors[1]);
      }
      resultSpan.textContent = `${game_result[0]} - ${game_result[1]}`;
    });
  });

  // Click first score card to trigger default
  if (scoreCardBtns.length) scoreCardBtns[0].click();
});

function deactivateAll() {
  document.querySelectorAll(".stat-bar").forEach((el) => el.classList.remove("active", "blue", "red"));
}

function deactivateBtns() {
  document.querySelectorAll(".stat-btn").forEach((btn) => btn.classList.remove("active"));
}

function handleScoreCardClick(btn) {
  const matchDataId = btn.id.slice(0, -4);
  const activeGameDetailsWrapper = document.getElementById(matchDataId);
  const arrows = document.querySelectorAll(".material-symbols-outlined.arrow");

  document.querySelectorAll(".game-details-wrapper").forEach((el) => el.classList.remove("active"));
  document.querySelectorAll(".score-card").forEach((el) => el.classList.remove("active"));
  arrows.forEach((el) => el.classList.remove("active"));
  deactivateBtns();
  deactivateAll();

  btn.classList.add("active");
  activeGameDetailsWrapper.classList.add("active");

  activeGameDetailsWrapper.querySelectorAll(".material-symbols-outlined.arrow").forEach((el) => el.classList.add("active"));
  activeGameDetailsWrapper.querySelectorAll(".rounded-line").forEach((el) => el.classList.add("active"));
  activeGameDetailsWrapper.querySelectorAll(".stat-diff-value").forEach((el) => el.classList.add("active"));

  const dmgBtn = activeGameDetailsWrapper.querySelector(".dmg-btn");
  if (dmgBtn) dmgBtn.click();
}

function handleStatClick(btn, statClass) {
  const wrapper = btn.closest(".game-details-wrapper");
  if (!wrapper) return;

  deactivateAll();
  deactivateBtns();
  btn.classList.add("active");

  const activeStatBars = wrapper.querySelectorAll(`.stat-bar.${statClass}`);
  const arrows = wrapper.querySelectorAll(".material-symbols-outlined.arrow");
  const roundedLines = wrapper.querySelectorAll(".rounded-line");
  const diffEls = wrapper.querySelectorAll(".stat-diff-value");

  activeStatBars.forEach((bar) => bar.classList.add("active"));

  const side = wrapper.dataset.team1Side;
  const colors = side === "blue side" ? ["blue", "red"] : ["red", "blue"];

  let idx = 1;
  activeStatBars.forEach((bar) => {
    bar.classList.add(idx <= 5 ? colors[0] : colors[1]);
    idx++;
  });

  const values = Array.from(activeStatBars).map((el) => {
    const text = el.textContent.trim().toUpperCase().replace("K", "");
    return parseFloat(text) * (el.textContent.includes("K") ? 1000 : 1);
  });

  const maxValue = Math.max(...values);
  activeStatBars.forEach((el, i) => {
    el.style.width = `${(values[i] / maxValue) * 100}%`;
  });

  arrows.forEach((el) => el.classList.remove("hidden", "red", "blue"));
  roundedLines.forEach((el) => el.classList.remove("red", "blue"));

  for (let i = 0; i < 5; i++) {
    const v1 = values[i];
    const v2 = values[i + 5];
    let diff = Math.abs(v1 - v2);
    diff = diff >= 1000 ? `${(diff / 1000).toFixed(1)}K` : diff.toFixed(0);

    diffEls[i].textContent = diff;

    if (v1 > v2) {
      arrows[i * 2].classList.add(colors[0]);
      arrows[i * 2 + 1].classList.add("hidden");
      roundedLines[i].classList.add(colors[0]);
    } else {
      arrows[i * 2 + 1].classList.add(colors[1]);
      arrows[i * 2].classList.add("hidden");
      roundedLines[i].classList.add(colors[1]);
    }
  }
}
