"""
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~ This file is part of a project for the course `Développement d'Algorithmes pour des Applications Réticulaires`
~ of the Master's degree in Computer Science at Sorbonne University.
~
~ Author: Eleni Pistiloglou
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """


import psycopg2 as db_connect
import json

host_name = 'localhost'
db_user = 'postgres'
db_password = '280411020118'
db_name = 'postgres'


def flatten_string(l: list[str]) -> str:
    flattened = ''
    for item in l:
        flattened += item
    return flattened

def initialize_database(input_file_name='index_decoded_clean.json', nbr_of_items=2794):
    """
    Inserts in the database table `documents` the id, title, authors, language 
    and rank of each book of the index.

    Args:
        input_file_name (string): the name of the file containing the index in json format.
        nbr_of_items (int): the number of documents in the index. 
    """
    
    with open(input_file_name, 'r', encoding='utf-8') as input_file:
    
        text = flatten_string(input_file.readlines())
        index = json.loads(text)

        for i in range(nbr_of_items):
            try:
                connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
                cursor = connection.cursor()
                query = "insert into documents (doc_id, title, authors, language, rank) values (" + index[i].get('id') + ", '" + index[i].get('title').replace("'"," ") + "', '" + index[i].get('authors').replace("'"," ") + "', '" + index[i].get('language') + "', -1);"
                cursor.execute(query) 
                cursor.close()
                connection.commit()
            except:
                print("ERROR: Error while retrieving document with id " + i)
                connection.rollback()

            connection.close()

def script2():
    with open('index_decoded_clean.json', 'r', encoding='utf-8') as f:
        text = flatten_string(f.readlines())
        index = json.loads(text)
     
        print(index[2748].get('id').replace("'"," "))
        print(index[2748].get('title').replace("'"," "))
        print(index[2748].get('authors').replace("'"," "))
        print(index[2748].get('language').replace("'"," "))


initialize_database()