// Node.js template literal SQLi
const { Pool } = require('pg');

async function searchUsers(term) {
    const query = `SELECT * FROM users WHERE name LIKE '%${term}%'`;
    const result = await pool.query(query);
    return result.rows;
}
