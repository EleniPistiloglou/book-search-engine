import psycopg2 as db_connect

host_name="localhost"
db_user="postgres"
db_password="280411020118"
db_name="postgres"


def key_mapping(res):
    return res[0]

connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
 
cursor = connection.cursor()

query = 'select b,c from sample where a=1;'

cursor.execute(query) 
#results = map(key_mapping, cursor.fetchall())
results = cursor.fetchall()
print(results)
"""
cursor.execute('insert into sample (id, name) values(1500, 1500);')
cursor.execute(query) 
results = cursor.fetchall()
print(results)
"""
cursor.close()

connection.commit()
connection.close()

