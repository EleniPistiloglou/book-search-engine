"""
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~ This file is part of a project for the course `Développement d'Algorithmes pour des Applications Réticulaires`
~ of the Master's degree in Computer Science at Sorbonne University.
~
~ Author: Eleni Pistiloglou
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """


import psycopg2 as db_connect
import db_credentials as db


def fetch_keywords(output_file_name='all_keywords.txt'):
    """
    Retrieves all keywords from the forward index and writes them in a file.

    Args:
        output_file_name (string): The name of the output file. 
    """

    with open(output_file_name, 'w', encoding='utf-8') as f:

        f.write('[')

        connection = db_connect.connect(host=db.host, user=db.user, password=db.password, database=db.name, port=5432)
        cursor = connection.cursor()
        query = "select keyword from findex group by keyword order by keyword;"
        cursor.execute(query) 
        keywords = cursor.fetchall()
        cursor.close()
        connection.close()

        for w in keywords:
            f.write('"' + w[0] + '"' + ",")

        f.write(']')