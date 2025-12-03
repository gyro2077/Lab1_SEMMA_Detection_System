// XSS Example 1: Reflected XSS via URL parameter
function displayWelcome() {
    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get('name');

    // VULNERABLE: Direct insertion without sanitization
    document.getElementById('welcome').innerHTML = `<h1>Welcome ${name}!</h1>`;
}

// XSS Example 2: Stored XSS via user comment
function addComment(comment) {
    const commentDiv = document.createElement('div');
    // VULNERABLE: innerHTML with user content
    commentDiv.innerHTML = comment;
    document.getElementById('comments').appendChild(commentDiv);
}

// XSS Example 3: DOM-based XSS
function search() {
    const query = document.getElementById('searchBox').value;
    // VULNERABLE: Direct DOM manipulation
    document.getElementById('results').innerHTML = `Results for: ${query}`;
}
