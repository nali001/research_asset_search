
# 2. Define the model serializer
from rest_framework import serializers
from notebook_search.models import GithubNotebookResult
from notebook_search.models import KaggleNotebookResult
from notebook_search.models import NotebookSearchRequest

class GithubNotebookResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubNotebookResult
        # Modify the fields to get a subset of fields to serialize
        fields = ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']


class KaggleNotebookResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = KaggleNotebookResult
        # Modify the fields to get a subset of fields to serialize
        fields = ['kaggle_id', 'name', 'file_name', 'description', 'html_url']
