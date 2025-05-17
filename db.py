import MySQLdb
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "passwd": "Sham@1609",
    "db": "inventory"
}

def init_db():
    conn = MySQLdb.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # 1. Create Product table (FIXED SYNTAX)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            product_description TEXT,
            price DECIMAL(10,2),
            quantity INT DEFAULT 0
        )
    ''')
    
    # 2. Create Location table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Location (
            location_id INT AUTO_INCREMENT PRIMARY KEY,
            location_name VARCHAR(255) NOT NULL,
            address TEXT
        )
    ''')
    
    # 3. Create ProductMovement table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ProductMovement (
            movement_id VARCHAR(50) PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            product_id INT NOT NULL,
            from_location INT,
            to_location INT,
            qty INT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Product(product_id),
            FOREIGN KEY (from_location) REFERENCES Location(location_id),
            FOREIGN KEY (to_location) REFERENCES Location(location_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_products():
    try:
        conn = MySQLdb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
      
        cursor.execute("SHOW TABLES")
        print(f"Tables in DB: {cursor.fetchall()}")  # Verify Product table exists
        
       
        cursor.execute("""
            SELECT product_id, product_name, price, quantity 
            FROM Product
            ORDER BY product_id
        """)
        
        products = cursor.fetchall()
        print(f"DEBUG: Fetched {len(products)} rows")  # Should match your SQL count
        return products
        
    except Exception as e:
        print(f"🚨 Database Error: {e}")
        return []
    finally:
        if conn:
            conn.close()
def get_product_by_id(product_id):
  
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('SELECT * FROM Product WHERE product_id = %s', (product_id,))
    product = cr.fetchone()
    conn.close()
    return product

def add_product(pd_name,quantity,pd_price):
  
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('''
        INSERT INTO inventory 
        (pd_name,quantity, pd_price) 
        VALUES (%s, %s, %s)
    ''', (pd_name,quantity,pd_price))
    conn.commit()
    conn.close()

def update_product(product_id, product_name):
  
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('''
        UPDATE Product 
        SET product_name = %s, description = %s 
        WHERE product_id = %s
    ''', (product_name, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):

    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('DELETE FROM Product WHERE product_id = %s', (product_id,))
    conn.commit()
    conn.close()


def get_all_locations():
    
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('SELECT * FROM Location')
    locations = cr.fetchall()
    conn.close()
    return locations

def get_location_by_id(location_id):
  
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('SELECT * FROM Location WHERE location_id = %s', (location_id,))
    location = cr.fetchone()
    conn.close()
    return location

def add_location(location_id, location_name, address=None):
  
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('INSERT INTO Location (location_id, location_name, address) VALUES (%s, %s, %s)', 
               (location_id, location_name, address))
    conn.commit()
    conn.close()

def update_location(location_id, location_name, address=None):
    
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('''
        UPDATE Location 
        SET location_name = %s, address = %s 
        WHERE location_id = %s
    ''', (location_name, address, location_id))
    conn.commit()
    conn.close()

def delete_location(location_id):
    
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('DELETE FROM Location WHERE location_id = %s', (location_id,))
    conn.commit()
    conn.close()

def get_all_movements():
   
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('''
        SELECT pm.movement_id, pm.timestamp, 
               p.product_name, 
               fl.location_name as from_location, 
               tl.location_name as to_location, 
               pm.qty
        FROM ProductMovement pm
        LEFT JOIN Product p ON pm.product_id = p.product_id
        LEFT JOIN Location fl ON pm.from_location = fl.location_id
        LEFT JOIN Location tl ON pm.to_location = tl.location_id
        ORDER BY pm.timestamp DESC
    ''')
    movements = cr.fetchall()
    conn.close()
    return movements

def get_movement_by_id(movement_id):
   
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('''
        SELECT pm.movement_id, pm.timestamp, 
               p.product_name, 
               fl.location_name as from_location, 
               tl.location_name as to_location, 
               pm.qty
        FROM ProductMovement pm
        LEFT JOIN Product p ON pm.product_id = p.product_id
        LEFT JOIN Location fl ON pm.from_location = fl.location_id
        LEFT JOIN Location tl ON pm.to_location = tl.location_id
        WHERE pm.movement_id = %s
    ''', (movement_id,))
    movement = cr.fetchone()
    conn.close()
    return movement

def add_movement(movement_id, product_id, qty, from_location=None, to_location=None):
 
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    
   
    if from_location and to_location and from_location == to_location:
        conn.close()
        raise ValueError("Cannot move to the same location")
    
    if qty <= 0:
        conn.close()
        raise ValueError("Quantity must be positive")
    
    if from_location:
        cr.execute('''
            SELECT COALESCE(SUM(
                CASE 
                    WHEN to_location = %s THEN qty
                    WHEN from_location = %s THEN -qty
                    ELSE 0
                END
            ), 0) AS balance
            FROM ProductMovement
            WHERE product_id = %s AND (to_location = %s OR from_location = %s)
            ''', (from_location, from_location, product_id, from_location, from_location))
        balance = cr.fetchone()[0]
        if balance < qty:
            conn.close()
            raise ValueError(f"Not enough stock in source location (available: {balance})")
    
    cr.execute('''
        INSERT INTO ProductMovement 
        (movement_id, product_id, from_location, to_location, qty) 
        VALUES (%s, %s, %s, %s, %s)
    ''', (movement_id, product_id, from_location, to_location, qty))
    
    conn.commit()
    conn.close()

def update_movement(movement_id, product_id, qty, from_location=None, to_location=None):
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('''
        UPDATE ProductMovement 
        SET product_id = %s, from_location = %s, to_location = %s, qty = %s
        WHERE movement_id = %s
    ''', (product_id, from_location, to_location, qty, movement_id))
    conn.commit()
    conn.close()

def delete_movement(movement_id):
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    cr.execute('DELETE FROM ProductMovement WHERE movement_id = %s', (movement_id,))
    conn.commit()
    conn.close()

def get_product_balances():
    conn = MySQLdb.connect(**DB_CONFIG)
    cr = conn.cursor()
    
    cr.execute('''
        SELECT 
            p.product_id,
            p.product_name,
            l.location_id,
            l.location_name,
            COALESCE(SUM(
                CASE 
                    WHEN pm.to_location = l.location_id THEN pm.qty
                    WHEN pm.from_location = l.location_id THEN -pm.qty
                    ELSE 0
                END
            ), 0) AS balance
        FROM Product p
        CROSS JOIN Location l
        LEFT JOIN ProductMovement pm ON 
            (pm.product_id = p.product_id AND 
             (pm.to_location = l.location_id OR pm.from_location = l.location_id))
        GROUP BY p.product_id, l.location_id
        HAVING balance > 0
        ORDER BY p.product_name, l.location_name
    ''')
    
    balances = cr.fetchall()
    conn.close()
    return balances

init_db()
