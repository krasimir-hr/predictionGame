function submitPredictions() {
    var form = document.getElementById('prediction-form');
    var numPendingMatches = parseInt(document.getElementById('num_pending_matches').value);

    // Loop through each pending match and append its input fields to the form data
    for (var i = 0; i < numPendingMatches; i++) {
        var team1Score = document.getElementsByName('team1_score_' + (i + 1))[0].value;
        var team2Score = document.getElementsByName('team2_score_' + (i + 1))[0].value;

        // Append input fields to form data
        var team1ScoreInput = document.createElement('input');
        team1ScoreInput.type = 'hidden';
        team1ScoreInput.name = 'team1_score_' + (i + 1);
        team1ScoreInput.value = team1Score;
        form.appendChild(team1ScoreInput);

        var team2ScoreInput = document.createElement('input');
        team2ScoreInput.type = 'hidden';
        team2ScoreInput.name = 'team2_score_' + (i + 1);
        team2ScoreInput.value = team2Score;
        form.appendChild(team2ScoreInput);
    }

    // Submit the form
    form.submit();
}
