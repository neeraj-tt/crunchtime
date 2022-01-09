//Create express app
const express = require('express');
const session = require('express-session')
const app = express();
const mongoose = require("mongoose");

mongoose.connect('mongodb://localhost/crunchtime', {useNewUrlParser: true});

let db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
    console.log("Connected to database.");
});

//View engine
app.set("view engine", "pug");

//Set up the routes
app.use(express.urlencoded({extended: true}));
app.use(express.static("public"));
app.use(express.json());


app.route("/")
.get((req, res) => {
    res.render("pages/index");
})
.post((req, res) => {
    var coll = db.collection("games").find({}).toArray(function(err, result) {
        if (err) throw err;
        //console.log(result);
        res.status(201).send(result);
        res.end();
    });    
});

// Start server
app.listen(3000);
console.log("Listening on port 3000");
