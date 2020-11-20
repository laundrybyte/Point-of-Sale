import sqlite3

def createdb():
    with sqlite3.connect("main.db") as db:
        cursor = db.cursor()

    # Create user db
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS userdb(
        userID INTEGER(4) PRIMARY KEY, 
        name VARCHAR(20) NOT NULL,
        passcode INTEGER(4) NOT NULL);
        ''')
    db.commit()

    # Create item db
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS itemdb(
        itemID INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(20) NOT NULL,
        price REAL NOT NULL);
        ''')
    db.commit()

    # Create transaction db
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactiondb(
        transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        transactiontime TEXT(50) NOT NULL,
        transactionitem TEXT(500) NOT NULL,
        transactionprice REAL NOT NULL,
        transactionmethod VARCHAR(10) NOT NULL,
        transactionuser VARCHAR(20) DEFAULT "System");
        ''')
    db.commit()

    # Create sales tax db
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salestaxdb(
        salestaxID INTEGER PRIMARY KEY AUTOINCREMENT,
        salestaxrate REAL NOT NULL DEFAULT 0.05);
    ''')
    db.commit()


    # Create default user "1212"
    cursor.execute('''
        INSERT OR IGNORE INTO userdb(userID,name,passcode)
        VALUES ("1111","Default User","1111")
    ''')
    db.commit()


    # Create default items
    cursor.execute('''
        INSERT OR IGNORE INTO itemdb(itemID,name,price)
        VALUES ("1","Blank Paper","0.01"), ("2","Black & White Copy", "0.10")
    ''')
    db.commit()

    # Create initial transaction
    cursor.execute('''
        INSERT OR IGNORE INTO transactiondb(transactionID,transactiontime,transactionitem,transactionprice,transactionmethod)
        VALUES ("0","0", "Create database", 0, "N/A")
    ''')
    db.commit()

    # Create default sales tax value
    cursor.execute('''
        INSERT OR IGNORE INTO salestaxdb(salestaxrate)
        VALUES ("0.05")''')
    db.commit()

createdb()