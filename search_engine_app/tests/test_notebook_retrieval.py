from django.test import TestCase
import requests
from notebook_search import notebook_retrieval

import os

# test_notebook_path = os.path.join(os.getcwd(), 'tests/Jupyter Notebook')
# test_index_name = 'test-index'

class TestNotebookRetrieval(TestCase):
    def test_notebook_retrieval(self):
        """
        Test the returned results
        """
        r =requests.get('http://127.0.0.1:7777/notebook_search/genericsearch/?term=cancer&page=1')
        searcher = notebook_retrieval.Genericsearch(r)
        results = searcher.genericsearch()
        print(results)
        # self.assertTrue(es.indices.exists(index = test_index_name), 'Indexing pipeline passed test.')
        # es.indices.delete(index = test_index_name)
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance