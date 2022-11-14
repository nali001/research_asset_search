
# serializers.py
''' Define the serializers for specific models
'''

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from notebooksearch.models import UserProfile
from notebooksearch.models import NotebookSearchParam
from notebooksearch.models import NotebookSearchLog
from notebooksearch.models import KaggleNotebook
from notebooksearch.models import NotebookSearchResult

from notebooksearch.models import NotebookDownloadParam
from notebooksearch.models import NotebookDownloadLog
from notebooksearch.models import NotebookDownloadResult

from notebooksearch.models import CellContent
from notebooksearch.models import GeneratedQuery
from notebooksearch.models import QueryGenerationLog
from notebooksearch.models import QueryGenerationResult

from notebooksearch.models import ContextSearchLog
from notebooksearch.models import ContextSearchResult

from notebooksearch.models import AnnotatedNotebook
from notebooksearch.models import RelevancyFeedbackLog

# ------------------- User Profile serializers --------------------    
class UserProfileSerializer(serializers.ModelSerializer): 
    ''' A serializer for serializing UserProfile data
    '''
    class Meta: 
        model = UserProfile
        fields = '__all__'
# -----------------------------------------------------------------


# ------------------- Notebook search serializers --------------------    
class NotebookSearchParamSerializer(serializers.ModelSerializer): 
    ''' A serialier for handling parameters of notebook search requests
    '''
    class Meta:
        model = NotebookSearchParam
        fields = '__all__'

class NotebookSearchLogSerializer(serializers.ModelSerializer): 
    ''' A serialier for handling notebook search requests
    '''
    class Meta:
        model = NotebookSearchLog
        fields = '__all__'

# class GithubNotebookResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GithubNotebookResult
#         # Modify the fields to get a subset of fields to serialize
#         fields = ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']


class KaggleNotebookSerializer(serializers.ModelSerializer):
    ''' A serliazer for serializing Kaggle notebooks
    '''
    class Meta:
        model = KaggleNotebook
        fields = ('docid', 'name', 'source', 'html_url', 'description', 'kaggle_id','file_name')


class KaggleNotebookSearchResultSerializer(serializers.ModelSerializer):
    ''' A nested serliazer for generating responses for notebook search using Kaggle notebooks

    It copys the notebook search request information received from the client and adds a list of notebook results
    '''
    results = KaggleNotebookSerializer(many=True)

    class Meta:
        model = NotebookSearchResult
        fields = '__all__'

# -----------------------------------------------------------------



# ------------------- Notebook download serializers --------------------    
class NotebookDownloadParamSerializer(serializers.ModelSerializer): 
    ''' A serialier for handling parameters of notebook download requests

    For `GET` and `POST`
    '''
    class Meta:
        model = NotebookDownloadParam
        fields = '__all__'

class NotebookDownloadLogSerializer(serializers.ModelSerializer): 
    ''' A serialier for handling notebook download `POST` requests data
    '''
    class Meta:
        model = NotebookDownloadLog
        fields = '__all__'


class NotebookDownloadResultSerializer(serializers.ModelSerializer):
    ''' A simple serliazer for generating responses for notebook download

    It simply returns the notebook soure file inside a models.TextField.  
    '''

    class Meta:
        model = NotebookDownloadResult
        fields = '__all__'

# -----------------------------------------------------------------


# ------------------- Query generation serializers --------------------
class CellContentSerializer(serializers.ModelSerializer): 
    ''' A serialier for handling cell contents 
    '''
    class Meta:
        model = CellContent
        fields = ('cell_type', 'cell_content')


class QueryGenetationLogSerializer(WritableNestedModelSerializer):
    ''' A nested serliazer for handling query generation requests
    '''
    cell_contents = CellContentSerializer(many=True, allow_null=True)
    class Meta:
        model = QueryGenerationLog
        fields = '__all__'


class GeneratedQuerySerializer(serializers.ModelSerializer): 
    ''' A serliazer for serializing geneted queries
    '''
    class Meta:
        model = GeneratedQuery
        fields = ('method', 'queries')

class QueryGenerationResultSerializer(serializers.ModelSerializer):
    ''' A nested serliazer for generating responses for query generation

    It generate one or more query for each 
    '''
    cell_contents = CellContentSerializer(many=True, allow_null=True)
    generated_queries = GeneratedQuerySerializer(many=True, allow_null=True)

    class Meta:
        model = QueryGenerationResult
        fields = '__all__'
# -----------------------------------------------------------------




# ------------------- Context-based search serializers --------------------
class ContextSearchLogSerializer(WritableNestedModelSerializer):
    ''' A nested serliazer for handling context search requests
    '''
    cell_contents = CellContentSerializer(many=True, allow_null=True)
    generated_queries = GeneratedQuerySerializer(many=True, allow_null=True)

    class Meta:
        model = ContextSearchLog
        fields = '__all__'

class KaggleContextSearchResultSerializer(serializers.ModelSerializer):
    ''' A nested serliazer for generating responses for context search using Kaggle notebooks

    It copys the context search request information received from the client and adds a list of notebook results
    '''
    cell_contents = CellContentSerializer(many=True, allow_null=True)
    generated_queries = GeneratedQuerySerializer(many=True, allow_null=True)
    search_results = KaggleNotebookSearchResultSerializer()

    class Meta:
        model = ContextSearchResult
        fields = '__all__'
# -----------------------------------------------------------------



# ------------------- Relevancy feedback serializers --------------------
class AnnotatedNotebookSerializer(serializers.ModelSerializer):
    ''' A serliazer for serializing annotated notebooks
    '''
    class Meta:
        model = AnnotatedNotebook
        fields = ('docid', 'name', 'source', 'html_url', 'description')


class RelevancyFeedbackLogSerializer(WritableNestedModelSerializer):
    ''' A nested serliazer for handling context search requests
    '''
    annotated_notebook = AnnotatedNotebookSerializer(allow_null=True)

    class Meta:
        model = RelevancyFeedbackLog
        fields = '__all__'
# -----------------------------------------------------------------
