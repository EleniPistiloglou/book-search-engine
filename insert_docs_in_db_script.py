"""
This file is part of a project that was developped for the course `Développement d'Algorithmes pour des Applications Réticulaires` of the Master's degree 
in Computer Science at Sorbonne University.

~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~ BD initialization script ~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~
~ Author: Eleni Pistiloglou
~
~ Inserts in the db table `documents` the id, title, authors, language and rank of each book.
~ 
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """


import psycopg2 as db_connect
import json

host_name="localhost"
db_user="postgres"
db_password="280411020118"
db_name="postgres"


def flatten_string(l):
    res = ''
    for item in l:
        res+=item
    return res

def script1():
    with open("index_decoded_clean.json", 'r', encoding="utf-8") as f:
        file = flatten_string(f.readlines())
        file_to_json = json.loads(file)
        for i in range(2749):
            """
            print(file_to_json[i].get('id'))
            print(file_to_json[i].get('title'))
            print(file_to_json[i].get('authors'))
            print(file_to_json[i].get('language'))
            """
            try:
                connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
                cursor = connection.cursor()
                query = "insert into documents (doc_id,title,authors,language,rank) values ("+file_to_json[i].get('id')+", '"+file_to_json[i].get('title').replace("'"," ")+"', '"+file_to_json[i].get('authors').replace("'"," ")+"', '"+file_to_json[i].get('language')+"', -1);"
                cursor.execute(query) 
                cursor.close()
                connection.commit()
            except:
                print(i)
                connection.rollback()
            connection.close()

def script2():
    with open("index_decoded_clean.json", 'r', encoding="utf-8") as f:
        file = flatten_string(f.readlines())
        file_to_json = json.loads(file)
     
        print(file_to_json[2748].get('id').replace("'"," "))
        print(file_to_json[2748].get('title').replace("'"," "))
        print(file_to_json[2748].get('authors').replace("'"," "))
        print(file_to_json[2748].get('language').replace("'"," "))
        


script1()