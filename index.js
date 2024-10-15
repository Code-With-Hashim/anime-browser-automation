// index.js
const express = require('express');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;

// Endpoint to call the Python script
app.get('/tpxsub', (req, res) => {
    const arg = req.params.arg;

    // Spawn a new child process to run the Python script
    const pythonProcess = spawn('python', ['tpxsub.py', arg]);

    let pythonResponse = '';

    // Capture the output from the Python script
    pythonProcess.stdout.on('data', (data) => {
        pythonResponse += data.toString();
    });

    // Handle any errors
    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    // When the Python script completes, send the response back
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            // If successful, send back the response as JSON
            res.json(JSON.parse(pythonResponse));
        } else {
            res.status(500).send(`Python script exited with code ${code}`);
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
