import sqlite3
from config import path_db
from db import queries


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.shopping_table)
    conn.commit()
    conn.close()

def add_product(product, quantity):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.insert_product, (product, quantity))
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id

def update_product(product_id, new_product = None, completed = None, quantity = None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if new_product is not None:
        cursor.execute(queries.update_product, (new_product, product_id)) #не перепутать последовательность
    elif completed is not None:
        cursor.execute('UPDATE shoplist SET completed = ? WHERE id = ?', (completed, product_id))
    elif quantity is not None:
        cursor.execute('UPDATE shoplist SET quantity = ? WHERE id = ?', (quantity, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_product, (product_id,))
    conn.commit()
    conn.close()

def get_products(filter_type):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    
    if filter_type == 'all':
        cursor.execute(queries.select_product)
    
    elif filter_type == 'completed':
        cursor.execute(queries.select_products_completed)
        
    
    elif filter_type == 'uncompleted':
        cursor.execute(queries.select_products_uncompleted)
        
    products = cursor.fetchall()
    conn.close()
    return products

def get_quantity(product_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.get_quantity, (product_id, ))
    quantity = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return quantity if quantity != None else 0

def count_products():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.count_products)
    product_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return product_count if product_count != None else 0