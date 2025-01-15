window.setInterval(getLive, 5000); // Fetch scores every 5 seconds

function getLive() {
    fetch('http://127.0.0.1:5000/live_scores') // Call the Flask backend
        .then((response) => response.json()) // Parse the JSON response
        .then((data) => {
            const gamesContainer = document.getElementById("games"); // The container for the games
            gamesContainer.innerHTML = ""; // Clear the previous game list

            // Loop through each game and display it
            data.forEach((game) => {
                const gameDiv = document.createElement("div");
                gameDiv.className = "game";

                gameDiv.innerHTML = `
                    <strong>${game.time}</strong><br>
                    ${game.homeTeam}: ${game.homeScore}<br>
                    ${game.awayTeam}: ${game.awayScore}<br>
                `;

                gamesContainer.appendChild(gameDiv);
            });
        })
        .catch((error) => {
            console.error("Error fetching live scores:", error);
        });
}
