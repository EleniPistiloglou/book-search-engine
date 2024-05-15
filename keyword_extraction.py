"""
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~ This file is part of a project that was developped for the course `Développement d'Algorithmes pour des Applications Réticulaires` of the Master's degree 
~ in Computer Science at Sorbonne University.
~ 
~ Author: Eleni Pistiloglou
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """

# note: split with multiple delimiters :
# re.split(';|,|.|:|?|!|--', str)

# we can also have a look at https://bookszone.net/books/principles-of-abstract-interpretation.html

import pandas as pd
import numpy as np
import requests
from sklearn.feature_extraction.text import CountVectorizer

import psycopg2 as db_connect

host_name = 'localhost'
db_user = 'postgres'
db_password = '123456789'
db_name = 'postgres'


def extract_keywords(id: int, lang='english') -> pd.DataFrame:
    """
    Extracts the keywords of a document.

    Args:
        id (int): The id of the document in the Gutenberg index.
        lang: The language of the document.
    
    Returns:
        Dataframe: A dataframe containing the extracted keywords.
    """
    if lang != 'english':
        raise ValueError("Language not supported.")

    doc = parse_document(str(id))
    # find keywords
    cv = CountVectorizer(stop_words=lang)
    cv_matrix = cv.fit_transform([doc]) 
    # create document term matrix
    return pd.DataFrame(cv_matrix.toarray(), index=['1'], columns=cv.get_feature_names_out())


def parse_document(id: int) -> str:
    """
    Fetches a book content from the Gutenberg website.

    Args:
        id (int): The id of the book.

    Returns:
        string: The book content in plain text format.
    """
    
    page = requests.get(url='https://www.gutenberg.org/cache/epub/' + id + '/pg' + id + '.txt')
    if not page.ok: page = requests.get('https://www.gutenberg.org/files/' + id + '/' + id + '-0.txt')
    
    # the books in .txt form follow this format: 
    # *** START OF THE PROJECT GUTENBERG EBOOK ***
    # book content
    # *** END OF THE PROJECT GUTENBERG EBOOK ***
    
    txt = page.text.split('***')[2]    \
        .replace('”', '"')       \
        .replace('“','"')        \
        .replace('_','')
    
    return txt


def unzip(l: list) -> list:
    return [pair[0] for pair in l], [pair[1] for pair in l]


def index(findex_name='findex', jaccard_name='graph', id_start=64192, id_end=67062, id_first=64192):
    """
    Populates the forward index table with the books having id within the specified range. 
    Calculates and stores in the database the jaccard distance between every new book and all existing ones.

    Args:
        findex_name (string): The name of the database table where the forward idex is stored.
        jaccard_name (string): The name of the table where the jaccard distance is stored.
        id_start (int): The id of the first book in the range. 
        id_end (int): The id of the last book in the range. 
        id_first (int): The lowest book id in the database. 
    """

    connection = db_connect.connect(host=host_name, user=db_user, password=db_password, database=db_name, port=5432)
    cursor = connection.cursor()

    unsuccessful = [] # ids of documents that couldn't be fetched from the server
    unsuccessful_i = [] # triplets of doc id, keyword, and weight that couldn't be inserted in the index
    usuccessful_j = []  # couples of ids of documents whose graph edge couldn't be stored

    for id in range(id_start, id_end+1, 1):
        try:
            keys_with_weights = extract_keywords(id) # this can throw an exception
            if keys_with_weights.empty : continue
            # add to forward index database
            keys = list(keys_with_weights)
            weights = keys_with_weights.to_numpy()[0]
            for k in range(len(keys)):
                try:
                    cursor.execute("insert into " + findex_name + " (doc, keyword, weight) values(" + str(id) + ", " + "'" + str(keys[k]) + "'" + ", " + str(weights[k]) + ");")
                    connection.commit()
                    print("DEBUG: inserted into ", findex_name, " the document ", id)
                except (Exception, db_connect.DatabaseError) as error:
                    print("Error in forward indexing, reverting all changes", error)
                    connection.rollback()
                    unsuccessful_i.append((id, keys[k], weights[k]))

            for id2 in range(id_first, id):
                try:
                    cursor.execute("select keyword, weight from " + findex_name + " where doc=" + str(id2) + ';')
                    keys2, weights2 = unzip(cursor.fetchall())
                    print("DEBUG:        fetched ", id2, " : ", keys2[0], "...", weights2[0])
                    if len(keys2) == 0 : continue

                    j = jaccard(keys, weights, keys2, weights2)
                    
                    # add weighted edge to graph database
                    if j != -1 and j < 0.7 : 
                        cursor.execute("insert into " + jaccard_name + " (doc2, doc1, weight) values(" + str(id) + ", " + str(id2) + ", " + str(j) + ");")
                        connection.commit()
                        
                except (Exception, db_connect.DatabaseError) as error:
                    print("Error in jaccard inserting, reverting all changes using rollback ", error)
                    connection.rollback()
                    usuccessful_j.append((id,id2))

        except (Exception): # failed to fetch document
            unsuccessful.append(id)

    cursor.close()
    connection.close()

    return (unsuccessful, unsuccessful_i, usuccessful_j)


def jaccard(a_labels, a_weights, b_labels, b_weights): 
    """
    Calculates the jaccard distance between two documents. Returns -1 if there is no correlation.

    Args:
        a_labels (): The keywords extracted from the first document.
        a_weights (): The weight of each keyword of the first document.
        b_labels (): The keywords extracted from the second document.
        b_weights (): The weight of each keyword of the second document.

    Returns:
        The jaccard distance, or -1 if there is no correlation.
    """

    numerator,denominator = 0, 0
    i, j = np.nditer(np.array(a_labels), flags=['refs_ok']), np.nditer(np.array(b_labels), flags=['refs_ok'])
    wi, wj = np.nditer(np.array(a_weights)), np.nditer(np.array(b_weights))

    while True:
        while i.value != j.value:
            if i.value < j.value:
                if i.iternext(): wi.iternext()
                else: return (numerator/denominator if denominator != 0 else -1)
            else:
                if j.iternext(): wj.iternext()
                else: return (numerator/denominator if denominator != 0 else -1)
        if wi.value > wj.value:
            numerator += (wi.value - wj.value)
            denominator += wi.value
        else :
            numerator += (wj.value - wi.value)
            denominator += wj.value
        if not i.iternext() or not wi.iternext() or not j.iternext() or not wj.iternext(): break
        
    #print("DEBUG: jaccard index : ", numerator/denominator if denominator!=0 else "no intersection found")
    return (numerator/denominator if denominator != 0 else -1)


if __name__ == "__main__":

    print(" * * * * * DATABASE INITIALIZATION * * * * * ")

    unsuccessfully_processed_docs, i, j = index(67151, 67300)
    
    print()
    with open('logs\\unsuccessfully_processed_docs.txt','w') as f:
        print("The following ids belong to documents that couldn't be successfully fetched from the Gutenberg project server:\n")
        for id in unsuccessfully_processed_docs:
            print(id)
            f.write(str(id) + '\n')

    print()
    with open('logs\\unsuccessfully_inserted_docs_index.txt','w') as f:
        print("The following ids belong to documents that couldn't be successfully inserted in the index:\n")
        for id in i:
            print(id)
            f.write(str(id) + '\n')
    
    print()
    with open('logs\\unsuccessfully_inserted_docs_graph.txt','w') as f:
        print("The following ids belong to documents that couldn't be successfully inserted in the index:\n")
        for id in j:
            print(id)
            f.write(str(id) + '\n')
    
    print()

# 64386, 65591