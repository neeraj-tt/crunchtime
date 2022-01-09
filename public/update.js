window.setInterval(getLive, 5000);

function getLive() {
    let req = new XMLHttpRequest();

	req.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 201){
			//alert("Successfully updated scores!");
			let data = req.responseText;
			let x = JSON.parse(data);
			//console.log(x);
			for (i = 0; i < x.length; i++) {
				let gameToEdit = document.getElementById(x[i].homeTeam + " vs " + x[i].awayTeam);
				if (gameToEdit == null) {
					let newDiv = document.createElement("div");
					newDiv.setAttribute("id", x[i].homeTeam + " vs " + x[i].awayTeam);
					newDiv.setAttribute("class", "game");
					document.getElementById("games").appendChild(newDiv);
					newDiv.innerHTML += x[i].time + "<br>" + x[i].homeTeam + ": " + x[i].homeScore + "<br>" + x[i].awayTeam + ": " + x[i].awayScore + "<br>" + + x[i].period + ", rem: " + x[i].rem + "<br>";
				} else {
					gameToEdit.innerHTML = x[i].time + "<br>" + x[i].homeTeam + ": " + x[i].homeScore + "<br>" + x[i].awayTeam + ": " + x[i].awayScore + "<br>" + + x[i].period + ", rem: " + x[i].rem + "<br>";
				}
				
				//console.log(x[i]);
			}
			// let liveGame = document.getElementById("current");
			// liveGame.innerHTML += "<iframe frameborder=0 height=100% width=100% src=\"http://givemenbastreams.com/nba.php?g=pistons\" allowfullscreen scrolling=no allowtransparency></iframe>"
			// liveGame.innerHTML += "<iframe frameborder=0 height=100% width=100% src=\"http://givemenbastreams.com/nba.php?g=pacers\" allowfullscreen scrolling=no allowtransparency></iframe>"
			// liveGame.innerHTML += "<iframe frameborder=0 height=100% width=100% src=\"http://givemenbastreams.com/nba.php?g=hornets\" allowfullscreen scrolling=no allowtransparency></iframe>"
			// liveGame.innerHTML += "<iframe frameborder=0 height=100% width=100% src=\"http://givemenbastreams.com/nba.php?g=celtics\" allowfullscreen scrolling=no allowtransparency></iframe>"
			// liveGame.innerHTML += "<iframe frameborder=0 height=100% width=100% src=\"http://givemenbastreams.com/nba.php?g=clippers\" allowfullscreen scrolling=no allowtransparency></iframe>"
			// liveGame.innerHTML += "<iframe frameborder=0 height=100% width=100% src=\"http://givemenbastreams.com/nba.php?g=suns\" allowfullscreen scrolling=no allowtransparency></iframe>"			
			//document.getElementById('games').innerHTML = data + "</br>";
		} else if (this.readyState == 4 && this.status == 401) {
			console.log("error getting live scores");
		}
	};

	req.open("POST", "/", true);
    req.setRequestHeader("Content-Type", "application/json")
	req.send();
}

// function getLive() {
//     db.collection("games").find(function(err, games) {
//         if(err) {
//             console.log(err);
//         } else {
//             console.log(games);
//         }
//     });    
// }