//Create express app
const express = require('express');
const session = require('express-session')
const app = express();
const mongoose = require("mongoose");

mongoose.connect("mongodb+srv://admin:admin@cluster0.aeen5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority");

let db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
    console.log("Connected to database.");
});

//View engine
app.set("view engine", "pug");

app.use(express.urlencoded({extended: true}));
app.use(express.static("public"));
app.use(express.json());

//Set up the routes
app.route("/")
.get((req, res) => {
    res.render("pages/index");
})
.post((req, res) => {
    var coll = db.collection("games").find({}).toArray(function(err, result) {
        if (err) throw err;
        res.status(201).send(result);
        console.log("yo");
        res.end();
    });    
});

// Start server
app.listen(process.env.PORT || 3000);
//console.log("Listening on port 3000");
