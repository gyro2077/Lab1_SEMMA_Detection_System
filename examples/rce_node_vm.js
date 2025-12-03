// Node.js vm module RCE
const vm = require('vm');

function runUserCode(code) {
    // VULNERABLE: User code in VM without sandbox
    vm.runInThisContext(code);
}
