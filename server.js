const express = require('express');
const app = express();

// Set up Pug as the view engine
app.set("view engine", "pug");

// Middleware to serve static files
app.use("/public", express.static("public"));

// Serve the homepage
app.get("/", (req, res) => {
    res.render("pages/index");
});

// Start the server
app.listen(3000, () => {
    console.log("Node.js server running on http://localhost:3000");
});
