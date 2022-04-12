import time
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

import psycopg2 as db_connect

host_name="localhost"
db_user="postgres"
db_password="280411020118"
db_name="postgres"


@csrf_exempt
def getBasicAPI(request, keyword=''):

    if request.method=='GET':

        print(keyword)
        t = time.time()
        keywords = request.GET.get('keyword').lower().split(' ')

        connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
        cursor = connection.cursor()

        query = "select doc_id, title, authors, sum(rank) as s from documents inner join findex on doc_id=doc where "
        for k in keywords:
            query += "keyword='"+k+"' or "
        query = query[:-4]
        query += " group by doc_id order by s desc;"
        print(query)

        cursor.execute(query) 
        documents = cursor.fetchall()
        cursor.close()
        connection.close()
        print(time.time()-t, " seconds")
        print(len(documents))

        return JsonResponse(documents, safe=False)


def or_subpatterns(s, regex=''):
    return s.split("|")


def getAdvancedAPI(request, regex=''):
    if request.method=='GET':
        t = time.time()

        regex = request.GET.get('regex').lower().split(' ')
        if len(regex)==1:

            regex = regex[0]

            # create a request using OR if the character | is present in the regex for better performance
            if regex.find('|') != -1:
                print('| found')
                subpatterns = or_subpatterns(regex)
                query = "select doc_id, title, authors, sum(rank) as s from documents inner join findex on doc_id=doc where "
                for sb in subpatterns:
                    if sb.find('*') != -1 or sb.find('.') != -1 or sb.find('+') != -1 or sb.find('&'):
                        query += "keyword  ~ '^"+sb+"$' or "
                    else:
                        query += "keyword  = '"+sb+"' or "
                query = query[:-4]
                query += " group by doc_id order by s desc;"
                #query = "select doc_id,title,sum(weight) as s from documents  inner join findex on doc_id=doc  where keyword ~ '"+regex+"' group by doc_id order by s desc;"
            
            # create a request for the ? character (which is presentt as & in the request)
            elif regex.find('&') != -1:
                print("? found")
                query = "select doc_id, title, authors, sum(rank) as s from documents inner join findex on doc_id=doc where "
                q1=regex.replace('&', '')
                regex=regex.split('&')
                q2 = regex[1]
                if q1.find('*') != -1 or q1.find('.') != -1 or q1.find('+') != -1 or q1.find('|') != -1:
                    query += "keyword  ~ '^"+q1+"$' or "
                else:
                    query += "keyword  = '"+q1+"' or "
                if q2.find('*') != -1 or q2.find('.') != -1 or q2.find('+') != -1 or q1.find('|') != -1:
                    query += "keyword  ~ '^"+q2+"$'"
                else:
                    query += "keyword  = '"+q2+"'"
                query += " group by doc_id order by s desc;"
            
            # create a request for all other characters
            else:
                query = "select doc_id, title, authors, sum(rank) as s from documents inner join findex on doc_id=doc where keyword~'^"+regex+"$' group by doc_id order by s desc;"

            connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
            cursor = connection.cursor()
            print(query)
            cursor.execute(query) 
            documents = cursor.fetchall()
            cursor.close()
            connection.close()
            print(time.time() - t, " seconds")
            print(len(documents))
            return JsonResponse(documents, safe=False)


def getRecomendations(request):
    doc='65000'
    query = "select doc_id, title, authors, rank from graph inner join documents on doc2=doc_id where doc1="+doc+" order by rank desc limit 10;"
    connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
    cursor = connection.cursor()
    cursor.execute(query) 
    documents = cursor.fetchall()
    cursor.close()
    connection.close()
    print(query)
    return JsonResponse(documents, safe=False)
