import pandas as pd
import numpy as np
import requests
from sklearn.feature_extraction.text import CountVectorizer

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

    return txt

def extract_keywords(id=64192):
    """
    Extracts the keywords of a document written in a given language
    """
    doc1 = parse_document(str(id))
    # find keywords
    cv2 = CountVectorizer(stop_words='english') # no other languages available
    cv_matrix2 = cv2.fit_transform([doc1]) 
    # create document term matrix
    return pd.DataFrame(cv_matrix2.toarray(), index=['1'], columns=cv2.get_feature_names_out())

def jaccard(a_labels, a_weights, b_labels, b_weights):
    """
    Calculates the jaccard distance between two documents
    """
    numerator,denominator = 0,0
    i,j = np.nditer(np.array(a_labels),flags=["refs_ok"]),np.nditer(np.array(b_labels),flags=["refs_ok"])
    wi,wj = np.nditer(np.array(a_weights)),np.nditer(np.array(b_weights))

    while True:
        while i.value != j.value:
            if i.value < j.value:
                if i.iternext():wi.iternext()
                else:return
            else:
                if j.iternext():wj.iternext()
                else:return
        #print(i.value,j.value)
        if wi.value > wj.value:
            numerator += (wi.value - wj.value)
            denominator += wi.value
        else :
            numerator += (wj.value - wi.value)
            denominator += wj.value
        if not i.iternext() or not wi.iternext() or not j.iternext() or not wj.iternext() : break
        
    print("jaccard index : ", numerator/denominator if denominator!=0 else "no intersection found")

res=extract_keywords()
l = ['dance', 'danced', 'dancing', 'danger', 'dangerous', 'dangerously','dangling', 'dans', 'dare','dared','dark', 'darkened', 'darkest', 'darling','darn','darted','darting', 'dashed', 'dashing','daughter','daughters','dawn']
ll = [2, 1, 3, 1, 2, 1,1, 1, 3,1,2, 2, 2, 2,1,1,1, 1, 1,2,2,1]
print(list(res)[0])
print(res.to_numpy()[0][0])
print(jaccard(list(res), res.to_numpy()[0], l, ll))