window.setInterval(getLive, 5000);

// variable to keep track of which stream to show
let oldGame = ""
let newGame = ""

let closestGame = -1;


function getLive() {
    let req = new XMLHttpRequest();

	req.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 201){
			let data = req.responseText;
			let x = JSON.parse(data);
			for (i = 0; i < x.length; i++) {				
				let gameToEdit = document.getElementById(x[i].homeTeam);
				if (gameToEdit == null) {
					let newDiv = document.createElement("div");
					newDiv.setAttribute("id", x[i].homeTeam);
					newDiv.setAttribute("class", "game");
					document.getElementById("games").appendChild(newDiv);
					newDiv.innerHTML += "<strong>" + x[i].time + "</strong><br>" + x[i].homeTeam + ": " + x[i].homeScore + "<br>" + x[i].awayTeam + ": " + x[i].awayScore + "<br>";
				} else {
					gameToEdit.innerHTML = "<strong>" + x[i].time + "</strong><br>" + x[i].homeTeam + ": " + x[i].homeScore + "<br>" + x[i].awayTeam + ": " + x[i].awayScore + "<br>";
				}
				// // if 4th quarter and game within 10
				// // OR game in overtime, then show this game
				// if ((x[i].period == 4 && Math.abs(x[i].homeScore - x[i].awayScore) < 10 && !(x[i].time.includes("Final"))) || x[i].period > 4 && !(x[i].time.includes("Final"))) {
				// 	//console.log(x[i].homeTeam, Math.abs(x[i].homeScore - x[i].awayScore));
				// 	newGame = x[i].homeTeam + " vs " + x[i].awayTeam;
				// 	let newGameElem = document.getElementById(newGame);
				// 	newGameElem.setAttribute("class", "gameShowing");
				// }				
			}

			// default stream
			for (j = 0; j < x.length; j++) {
				if (x[j].rem != "") {
					let curr = x[j];
					let match = curr.rem.match(/\d+/g);
					mins = parseInt(match[0]);
					sec = parseInt(match[1]);
					ms = parseInt(match[2]);

					sec += (60 * mins);
					if (curr.period == 1) {
						sec += (36 * 60);
					} else if (curr.period == 2) {
						sec += (24 * 60);
					} else if (curr.period == 3) {
						sec += (12 * 60);
					}
					// switch game if game in 4th quarter or overtime, within 10 and with less time remaining than current game
					// or if current game is over
					if (closestGame == -1 || (sec < closestGame && (Math.abs(x[j].homeScore - x[j].awayScore) < 10) && x[j].period >= 4) || closestGame == 0) {
					// if (closestGame == -1 || (sec < closestGame)) {
						closestGame = sec;
						newGame = x[j].homeTeam;
						let newGameElem = document.getElementById(newGame);
						newGameElem.setAttribute("class", "gameShowing");
						if (newGame != oldGame) {
							if (oldGame != "") {
								let oldGameElem = document.getElementById(oldGame);
								oldGameElem.setAttribute("class", "game");
							}
							oldGame = newGame;
							let temp = newGame.split(" ");
							let gameURL = temp[temp.length-1].toLowerCase();
							let liveGame = document.getElementById("current");
							liveGame.innerHTML = "<iframe frameborder=0 height=80% width=80% class=\"player\" src=\"https://givemenbastreams.com/nba.php?g=" + gameURL + "\" allow =\"autoplay\" allowfullscreen scrolling=no allowtransparency></iframe>"
						}
					}
				}
			}
		} else if (this.readyState == 4 && this.status == 401) {
			console.log("error getting live scores");
		}
	};

	req.open("POST", "/", true);
    req.setRequestHeader("Content-Type", "application/json")
	req.send();
}