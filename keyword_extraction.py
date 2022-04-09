"""
This file is part of a project that was developped for the course `Développement d'Algorithmes pour des Applications Réticulaires` of the Master's degree 
in Computer Science at Sorbonne University.

~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~ BD initialization script ~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~
~
~ Author: Eleni Pistiloglou
~
~ Retrieves each book whose id falls within the specified interval, stores its forward index in the table findex,
~ and the new edges it creates, weighted by the jaccard coefficient of all other documents, in the table graph 
~ 
~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~  """


# note: split with multiple delimiters :
# re.split(';|,|.|:|?|!|--', str)

# we can also have a look at https://bookszone.net/books/principles-of-abstract-interpretation.html

import pandas as pd
import numpy as np
import requests
from sklearn.feature_extraction.text import CountVectorizer

import psycopg2 as db_connect


def extract_keywords(id):
    """
    Extracts the keywords of a document written in a given language
    """
    doc1 = parse_document(str(id))
    # find keywords
    cv2 = CountVectorizer(stop_words='english') # no other languages available
    cv_matrix2 = cv2.fit_transform([doc1]) 
    # create document term matrix
    return pd.DataFrame(cv_matrix2.toarray(), index=['1'], columns=cv2.get_feature_names_out())


def parse_document(id):
    """
    Parses the text of a book to extract its keywords
    """
    page = requests.get(url='https://www.gutenberg.org/cache/epub/'+id+'/pg'+id+'.txt')
    if not page.ok : page = requests.get('https://www.gutenberg.org/files/'+id+'/'+id+'-0.txt')
    # the books in .txt form follow this format: 
    # *** START OF THE PROJECT GUTENBERG EBOOK ***
    # book content
    # *** END OF THE PROJECT GUTENBERG EBOOK ***
    txt = page.text.split('***')[2]    \
        .replace('”', '"')       \
        .replace('“','"')        \
        .replace('_','')

    #print(txt)
    return txt


def unzip(l):
    #print("DEBUG: arg:",l)
    return [pair[0] for pair in l],[pair[1] for pair in l]

def index(id_start=64192, id_end=67062):
    """
    Creates the forward index (table name:findex) and the jaccard distance database (table name:graph) in the db 'postgre'
    """

    id_of_first_document = 64192

    host_name="localhost"
    db_user="postgres"
    db_password="280411020118"
    db_name="postgres"

    connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
    cursor = connection.cursor()

    unsuccessful = [] # to store ids of documents that couldn't be fetched from the server
    unsuccessful_i = [] # to store triples of doc id, keyword, and weight that couldn't be inserted in the index
    usuccessful_j = []  # to store couples of ids of documents whose graph edge couldn't be stored
    for id in range(id_start,id_end+1,1):
        try:
            keys_with_weights = extract_keywords(id) # this can throw an exception
            if keys_with_weights.empty : continue
            # add to forward index database
            keys = list(keys_with_weights)
            weights = keys_with_weights.to_numpy()[0]
            for k in range(len(keys)):
                try:
                    cursor.execute("insert into findex (doc, keyword, weight) values("+str(id)+", "+"'"+str(keys[k])+"'"+", "+str(weights[k])+");")
                    connection.commit()
                    #print("DEBUG: inserted into findex doc",id)
                except (Exception, db_connect.DatabaseError) as error:
                    print("Error in forward indexing, reverting all changes using rollback ", error)
                    connection.rollback()
                    unsuccessful_i.append((id,keys[k],weights[k]))

            for doc2 in range(id_of_first_document, id):
                try:
                    cursor.execute('select keyword, weight from findex where doc='+str(doc2)+';')
                    keys2,weights2 = unzip(cursor.fetchall())
                    #print("DEBUG:        fetched ",doc2," : ",keys2[0],"...",weights2[0])
                    if len(keys2)==0 : continue
                    j = jaccard(keys, weights, keys2, weights2) # returns -1 if no correlation
                    # add weighted edge to graph database
                    if j!=-1 and j<0.7 : 
                        cursor.execute('insert into graph (doc2, doc1, weight) values('+str(id)+', '+str(doc2)+', '+str(j)+');')
                        connection.commit()
                        
                except (Exception, db_connect.DatabaseError) as error:
                    print("Error in jaccard inserting, reverting all changes using rollback ", error)
                    connection.rollback()
                    usuccessful_j.append((id,doc2))

        except (Exception): # failed to fetch document
            unsuccessful.append(id)

    cursor.close()
    connection.close()

    return (unsuccessful, unsuccessful_i, usuccessful_j)


def jaccard(a_labels, a_weights, b_labels, b_weights): 
    """
    Calculates the jaccard distance between two documents
    """
    #a_labels = np.array(a.columns)
    #b_labels = np.array(b.columns)
    #a_labels_set = set(a.columns)
    #a_labels_set = set(a.columns)
    #b_labels_set = set(b.columns)
    #print(a_labels, "\n", b_labels, "\n\nINTERSECTION\n\n", a_labels_set.intersection(b_labels_set))
    #a_weights = a.to_numpy()[0]
    #b_weights = b.to_numpy()[0]

    numerator,denominator = 0,0
    i,j = np.nditer(np.array(a_labels),flags=["refs_ok"]),np.nditer(np.array(b_labels),flags=["refs_ok"])
    wi,wj = np.nditer(np.array(a_weights)),np.nditer(np.array(b_weights))

    while True:
        while i.value != j.value:
            if i.value < j.value:
                if i.iternext():wi.iternext()
                else:return (numerator/denominator if denominator!=0 else -1)
            else:
                if j.iternext():wj.iternext()
                else:return (numerator/denominator if denominator!=0 else -1)
        #print(i.value,j.value)
        if wi.value > wj.value:
            numerator += (wi.value - wj.value)
            denominator += wi.value
        else :
            numerator += (wj.value - wi.value)
            denominator += wj.value
        if not i.iternext() or not wi.iternext() or not j.iternext() or not wj.iternext() : break
        
    #print("jaccard index : ", numerator/denominator if denominator!=0 else "no intersection found")
    return (numerator/denominator if denominator!=0 else -1)


if __name__=="__main__":
    unsuccessfully_processed_docs, i, j = index(67151,67300)

    with open('logs\\unsuccessfully_processed_docs.txt','w') as f:
        print("The following ids belong to documents that couldn't be successfully fetched from the Gutenberg project server:\n")
        for id in unsuccessfully_processed_docs:
            print(id)
            f.write(str(id)+"\n")

    print()
    with open('logs\\unsuccessfully_inserted_docs_index.txt','w') as f:
        print("The following ids belong to documents that couldn't be successfully inserted in the index:\n")
        for id in i:
            print(id)
            f.write(str(id)+"\n")
    
    print()
    with open('logs\\unsuccessfully_inserted_docs_graph.txt','w') as f:
        print("The following ids belong to documents that couldn't be successfully inserted in the index:\n")
        for id in j:
            print(id)
            f.write(str(id)+"\n")


# 64386, 65591