document.addEventListener("DOMContentLoaded", () => {
    window.setInterval(getLive, 5000); // Fetch scores every 5 seconds
});

function getLive() {
    fetch('http://127.0.0.1:5001/live_scores') // Call the Flask backend
        .then((response) => response.json()) // Parse the JSON response
        .then((data) => {
            const gamesContainer = document.getElementById("games"); // The container for the games

            // Loop through each game
            data.updates.forEach((game) => {
                const gameId = (game.homeTeam).toLowerCase().trim() + "_game";
                let gameDiv = document.getElementById(gameId);
                
                if (!gameDiv) {
                    gameDiv = document.createElement("div");
                    gameDiv.className = "game";
                    gameDiv.id = gameId;

                    gameDiv.innerHTML = `
                        <strong class="game-time">${game.time}</strong><br>
                        <img class="team-logo" src="/public/images/teamLogos/${game.homeTricode}.png">
                        <span class="home-team">${game.homeCity} ${game.homeTeam}</span>:
                        <span class="home-score">${game.homeScore}</span><br>
                        <img class="team-logo" src="/public/images/teamLogos/${game.awayTricode}.png">
                        <span class="away-team">${game.awayCity} ${game.awayTeam}</span>:
                        <span class="away-score">${game.awayScore}</span><br>                        
                    `;

                    gamesContainer.appendChild(gameDiv);
                } else {
                    // If game already exists, update content
                    gameDiv.querySelector(".game-time").textContent = game.time;
                    gameDiv.querySelector(".home-score").textContent = game.homeScore;
                    gameDiv.querySelector(".away-score").textContent = game.awayScore;
                }  
            });

            const oldGameElems = Array.from(document.getElementsByClassName("gameShowing"));
            const newGame = data.mostExciting;
            const newGameElem = document.getElementById(newGame + "_game");

            if (!newGameElem || data.mostExciting == "None") {
                return; // Exit if the new game element is not found
            }

            if (oldGameElems.length === 0) {
                // No game is currently highlighted
                newGameElem.setAttribute("class", "gameShowing");
                document.getElementById("current").querySelector(".player").style.visibility = "hidden";

            } else {
                const currentGameElem = oldGameElems[0];
                if (newGameElem.getAttribute("id") !== currentGameElem.getAttribute("id")) {
                    // Highlight the new game and reset the old one
                    currentGameElem.setAttribute("class", "game");
                    newGameElem.setAttribute("class", "gameShowing");
                } else {
                    return;     // Game already highlighted
                }
            }

            // Update the stream source
            const stream = document.getElementById("stream");
            stream.style.visibility = "visible"
            const newStream = `https://givemereddit.eu/nba/${data.mostExciting}.html`;
            if (stream.src !== newStream) {
                stream.src = newStream;
            }
        })
        .catch((error) => {
            console.error("Error fetching live scores:", error);
        });
}
