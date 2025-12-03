// Node.js string concatenation SQLi
const mysql = require('mysql');

function getUser(userId) {
    const query = "SELECT * FROM users WHERE id = " + userId;
    connection.query(query, (error, results) => {
        console.log(results);
    });
}
