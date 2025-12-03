// DOM-based XSS in search
function displaySearchResults() {
    const query = document.getElementById('searchInput').value;
    // VULNERABLE: Direct DOM manipulation
    document.getElementById('results').innerHTML = 
        '<h2>Results for: ' + query + '</h2>';
}
