
# 2. Define the model serializer
from rest_framework import serializers
from notebook_search.models import NotebookResult

class NotebookResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookResult
        # Modify the fields to get a subset of fields to serialize
        fields = ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']
        # fields = ['name', 'full_name']


