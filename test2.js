//Create express app
const express = require('express');
const app = express();

app.get('/', (req, res) => {

    const { spawn } = require('child_process');
    const pyProg = spawn('python', ['live.py']);

    pyProg.stdout.on('data', function(data) {

        console.log(data.toString());
        res.write(data);
        res.end();
    });
})

// Start server
app.listen(3000);
console.log("Listening on port 3000");
