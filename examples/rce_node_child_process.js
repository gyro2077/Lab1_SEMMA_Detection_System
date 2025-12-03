// Node.js child_process.exec RCE
const { exec } = require('child_process');

function convertFile(filename) {
    // VULNERABLE: Command injection
    exec(`convert ${filename} output.pdf`, (error, stdout) => {
        console.log(stdout);
    });
}
