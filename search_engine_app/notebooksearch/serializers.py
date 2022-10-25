
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

from notebooksearch.models import QueryGenerationLog
from notebooksearch.models import CellContent
from notebooksearch.models import GeneratedQuery
from notebooksearch.models import QueryGenerationResult


# class GithubNotebookResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GithubNotebookResult
#         # Modify the fields to get a subset of fields to serialize
#         fields = ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']


# class NotebookSearchRequestSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = NotebookSearchRequest
#         # Modify the fields to get a subset of fields to serialize
#         fields = '__all__'

# class NotebookSearchRequestLogSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = NotebookSearchRequestLog
#         # Modify the fields to get a subset of fields to serialize
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer): 
#     class Meta: 
#         model = ClientUser
#         fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer): 
    ''' A serializer for serializing UserProfile data
    '''
    class Meta: 
        model = UserProfile
        fields = '__all__'



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

class KaggleNotebookSerializer(serializers.ModelSerializer):
    ''' A serliazer for serializing Kaggle notebooks
    '''
    class Meta:
        model = KaggleNotebook
        fields = ('kaggle_id', 'name', 'file_name', 'html_url', 'description')


class KaggleNotebookSearchResultSerializer(serializers.ModelSerializer):
    ''' A nested serliazer for generating responses for notebook search using Kaggle notebooks

    It copys the notebook search request information received from the client and adds a list of notebook results
    '''
    results = KaggleNotebookSerializer(many=True)

    class Meta:
        model = NotebookSearchResult
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
        fields = ('generation_method', 'generated_queries')

class QueryGenerationResultSerializer(serializers.ModelSerializer):
    ''' A nested serliazer for generating responses for query generation

    It generate one or more query for each 
    '''
    cell_contents = CellContentSerializer(many=True)
    generation_results = GeneratedQuerySerializer(many=True)

    class Meta:
        model = QueryGenerationResult
        fields = '__all__'
# -----------------------------------------------------------------




# # ------------------- Context-based search serializers --------------------
# class ContextSearchSession(BaseUser): 
#     ''' Context-based search session
#     '''



# # -----------------------------------------------------------------



# # ------------------- Relevancy feedback serializers --------------------
# class RelevancyFeedbackRequest(NotebookSearchRequest): 
#     num_stars = models.IntegerField()

# # class RelevancyFeedbackLog(NotebookSearchRequest, BaseNotebook): 
# #     num_stars = models.IntegerField()
# # -----------------------------------------------------------------
