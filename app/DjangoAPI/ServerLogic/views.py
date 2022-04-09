import re
import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from ServerLogic.models import Documents
from ServerLogic.serializers import DocumentSerializer

import psycopg2 as db_connect
import json

host_name="localhost"
db_user="postgres"
db_password="280411020118"
db_name="postgres"


@csrf_exempt
def getBasicAPI(request, keyword=''):
    if request.method=='GET':
        
        connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
        cursor = connection.cursor()
        query = "select doc_id, title from documents inner join findex on doc_id=doc where keyword='"+keyword+"' order by weight desc;"
        cursor.execute(query) 
        documents = cursor.fetchall()
        cursor.close()
        connection.close()
        return JsonResponse(documents, safe=False)

def or_subpatterns(s):
    return s.split("|")

def getAdvancedAPI(request, regex=''):
    if request.method=='GET':

        # create a request using OR if the character | is present in the regex for better performance
        if regex.find('|') != -1:

            t = time.time()
            subpatterns = or_subpatterns(regex)
            query = "select doc_id, title, sum(weight) as s from documents inner join findex on doc_id=doc where "
            for sb in subpatterns:
                if sb.find('*') != -1 or sb.find('.') != -1 or sb.find('+') != -1:
                    query += "keyword  ~ '"+sb+"' or "
                else:
                    query += "keyword  = '"+sb+"' or "
            query = query[:-4]
            query += " group by doc_id order by s desc;"
        
        # create request for the + character
        
        # create a request for the rest of the characters characters
        else:
            query = "select doc_id, title, sum(weight) as s from documents inner join findex on doc_id=doc where keyword~'"+regex+"' group by doc_id order by s desc;"

        connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
        cursor = connection.cursor()
        cursor.execute(query) 
        documents = cursor.fetchall()
        cursor.close()
        connection.close()
        print(time.time() - t, " seconds")
        return JsonResponse(documents, safe=False)

  
