import psycopg2 as db_connect

host_name="localhost"
db_user="postgres"
db_password="280411020118"
db_name="postgres"

with open("all_keywords.txt", 'w', encoding='utf-8') as f:
    f.write('[')
    connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
    cursor = connection.cursor()
    query = "select keyword from findex group by keyword order by keyword;"
    cursor.execute(query) 
    keywords = cursor.fetchall()
    cursor.close()
    connection.close()
    print(keywords[0])
    for w in keywords:
        f.write('"'+w[0]+'"'+",")
    f.write('""]')