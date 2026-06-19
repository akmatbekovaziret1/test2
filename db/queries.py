# C-R-U-D: Create, Read, Update, Delete

shopping_table = """
    CREATE TABLE IF NOT EXISTS shoplist (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        product TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        quantity INTEGER DEFAULT 0
    )
"""

# Create

insert_product = 'INSERT INTO shoplist (product, quantity) VALUES (?, ?)'

# Read
select_product = 'SELECT * FROM shoplist'

count_products = 'SELECT SUM(quantity) FROM shoplist'

get_quantity = 'SELECT quantity FROM shoplist WHERE id = ?'

select_products_completed = """
    SELECT id, product, completed, quantity
    FROM shoplist
    WHERE completed = 1
"""

select_products_uncompleted = """
    SELECT id, product, completed, quantity
    FROM shoplist
    WHERE completed = 0
"""


# Update

update_product = 'UPDATE shoplist SET product = ? WHERE id = ?'

# Delete

delete_product = 'DELETE FROM shoplist WHERE id = ?'



