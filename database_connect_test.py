import psycopg2 as db_connect
import db_credentials as db

def key_mapping(res):
    return res[0]

def test_select():
    connection = db_connect.connect(host=db.host, user=db.user, password=db.password, database=db.name, port=db.port)
    cursor = connection.cursor()
    query = 'select b,c from sample where a=1;'
    cursor.execute(query) 
    
    #results = map(key_mapping, cursor.fetchall())
    results = cursor.fetchall()
    print(results)
    
    cursor.close()
    connection.commit()
    connection.close()

def test_insert():
    connection = db_connect.connect(host=db.host, user=db.user, password=db.password, database=db.name, port=db.port)
    cursor = connection.cursor()
    cursor.execute('insert into sample (id, name) values(1500, 1500);')

    results = cursor.fetchall()
    print(results)
    
    cursor.close()
    connection.commit()
    connection.close()

