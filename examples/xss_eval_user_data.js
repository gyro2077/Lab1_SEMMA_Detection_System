// eval() with user data XSS
function executeUserScript(userCode) {
    // EXTREMELY VULNERABLE
    eval(userCode);
}

const code = new URLSearchParams(location.search).get('code');
executeUserScript(code);
