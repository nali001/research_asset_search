
# 2. Define the model serializer
from rest_framework import serializers
from notebook_search.models import NotebookResult

class NotebookResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookResult
        fields = ['name', 'alias']


