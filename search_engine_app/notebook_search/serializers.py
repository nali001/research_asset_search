
# 2. Define the model serializer
from rest_framework import serializers
from notebook_search.models import NotebookResultGithub

class NotebookResultGithubSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookResultGithub
        # Modify the fields to get a subset of fields to serialize
        fields = ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']
        # fields = ['name', 'full_name']


