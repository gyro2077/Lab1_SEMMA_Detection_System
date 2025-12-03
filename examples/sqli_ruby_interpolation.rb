# Ruby string interpolation SQLi
require 'sqlite3'

def search_products(keyword)
  db = SQLite3::Database.new "products.db"
  query = "SELECT * FROM products WHERE name LIKE '%#{keyword}%'"
  db.execute(query)
end
