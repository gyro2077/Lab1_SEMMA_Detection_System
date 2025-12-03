app.get('/search', (req, res) => {
    const q = "SELECT * FROM products WHERE name = '" + req.q.name + "'";
    db.q(q, (err, results) => {
        res.json(results);
    });
});