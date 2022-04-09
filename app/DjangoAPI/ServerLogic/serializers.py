from curses.ascii import EM
from rest_framework import serializers
from ServerLogic.models import Documents

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Documents
        fields=('doc', 'keyword', 'weight')

