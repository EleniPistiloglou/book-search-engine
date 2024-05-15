"""
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~ This file is part of a project that was developped for the course `Développement d'Algorithmes pour des Applications Réticulaires` of the Master's degree 
~ in Computer Science at Sorbonne University.
~
~ Author: Eleni Pistiloglou
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """


import psycopg2 as db_connect

host_name = "localhost"
db_user = "postgres"
db_password = "280411020118"
db_name = "postgres"


def fetch_keywords(output_file_name='all_keywords.txt'):
    """
    Retrieves all keywords from the forward index and writes them in a file.

    Args:
        output_file_name (string): The name of the output file. 
    """

    with open(output_file_name, 'w', encoding='utf-8') as f:

        f.write('[')

        connection = db_connect.connect(host=host_name, user=db_user, password=db_password, database=db_name, port=5432)
        cursor = connection.cursor()
        query = "select keyword from findex group by keyword order by keyword;"
        cursor.execute(query) 
        keywords = cursor.fetchall()
        cursor.close()
        connection.close()

        for w in keywords:
            f.write('"' + w[0] + '"' + ",")

        f.write(']')