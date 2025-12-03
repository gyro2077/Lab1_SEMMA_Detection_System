app.get('/search', (req, res) => {
  const query = "SELECT * FROM products WHERE name = '" + req.query.name + "'";
  db.query(query, (err, results) => {
    res.json(results);
  });
});