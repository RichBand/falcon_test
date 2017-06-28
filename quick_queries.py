import sqlite3, json

def Main():
    conn = sqlite3.connect('Simpsons.db')
    cur = conn.cursor()
    # result = cur.execute('SELECT * FROM characters').fetchall()
    # result = cur.execute('DELETE FROM characters WHERE id = 1;').fetchall()
    result = cur.execute('DROP TABLE characters')
    # result = json.dumps(result)
    print(result)
    conn.commit()
    cur.close()

Main()
