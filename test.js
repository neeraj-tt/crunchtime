const express = require('express');
const session = require('express-session')
const app = express();

app.route("/")
.get((req, res) => {
    res.send("hi");
})

app.listen(3000);
console.log("Listening on port 3000");