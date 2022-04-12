from django.urls import re_path 
from ServerLogic import views


urlpatterns=[
    re_path(r'^basic/([a-zA-Z0-9]*)$', views.getBasicAPI), 
    re_path(r'^advanced/(.*)$', views.getAdvancedAPI), 
    re_path(r'^recomendations$', views.getRecomendations)
]
