app.get('/search', (req, res) => {
    const sql = "SELECT * FROM products WHERE name = '" + req.sql.name + "'";
    db.sql(sql, (err, results) => {
        res.json(results);
    });
});