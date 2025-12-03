// FIXME: Add input sanitization
const { exec } = require('child_process');
exec(`ls ${userPath}`, (error, stdout) => {
  console.log(stdout);
});