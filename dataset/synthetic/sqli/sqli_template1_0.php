# TODO: Fix security issue
def get_product(product_id):
  sql = f"SELECT * FROM products WHERE id = {product_id}"
  cursor.execute(sql)