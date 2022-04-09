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

# Create your views here.
@csrf_exempt
def getBasicAPI(request, keyword=''):
    if request.method=='GET':
        # get doc ids from database
        connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
        cursor = connection.cursor()
        # query = "select doc,weight from findex where keyword='"+keyword+"' order by weight desc;"
        query = "select doc_id, title from documents inner join findex on doc_id=doc where keyword='"+keyword+"' order by weight desc;"
        cursor.execute(query) 
        documents = cursor.fetchall()
        print(keyword)
        cursor.close()
        connection.close()
        print(len(documents))



        # get document url from database
        """with open("index_decoded_clean.json") as f:
            #response = f.
            pass"""
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
            #query = "select doc_id,title,sum(weight) as s from documents  inner join findex on doc_id=doc  where keyword ~ '"+regex+"' group by doc_id order by s desc;"
        
        # create a request for the * character
        elif regex.find("*") != -1:

            t = time.time()
            """
            pattern = re.compile(regex, re.IGNORECASE)
            with open("../../all_keywords.txt", "r", encoding='utf-8') as f:
                keywords_text = f.readlines()
            keywords = json.loads(keywords_text[0])
            query = "select doc_id, title, sum(weight) as s from documents inner join findex on doc_id=doc where "
            for w in keywords:
                if pattern.match(w) != None:
                    query += "keyword  = '"+w+"' or "
            query = query[:-4]
            query += " group by doc_id order by s desc;"
            """
            query = "select doc_id,title,sum(weight) as s from documents  inner join findex on doc_id=doc  where keyword ~ '"+regex+"' group by doc_id order by s desc;"
        else:
            query = "select doc_id, title, sum(weight) as s from documents inner join findex on doc_id=doc where keyword~'"+regex+"' group by doc_id order by s desc;"

        connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name,port=5432)
        cursor = connection.cursor()
        # query = "select doc,weight from findex where keyword ~ '"+keyword+"' order by weight desc;"
        print(query)
        cursor.execute(query) 
        documents = cursor.fetchall()
        cursor.close()
        connection.close()
        print(len(documents))
        print(time.time() - t, " seconds")
        return JsonResponse(documents, safe=False)

    """
    elif request.method=='POST':
        dept_data=JSONParser().parse(request)
        depts_serializer = DepartmentSerializer(data=dept_data)
        if depts_serializer.is_valid():
            depts_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("failed to add", safe=False)
    elif request.method=='PUT':
        pass
    elif request.method=='DELETE':
        dept = Departments.objects.get(deptId=id)
        dept.delete()
        return JsonResponse("Deleted Successfully", safe=False)"""