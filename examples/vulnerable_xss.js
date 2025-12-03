// Ejemplo de código vulnerable a XSS
function displayUserComment(comment) {
    // Vulnerable: inserción directa de input del usuario
    document.getElementById('comments').innerHTML = comment;
}

function searchResults(query) {
    // Vulnerable: refleja input sin sanitizar
    document.write("<h2>Resultados para: " + query + "</h2>");
}

// Vulnerable: eval de datos del usuario
function executeUserCode() {
    var userCode = document.getElementById('code-input').value;
    eval(userCode);
}
