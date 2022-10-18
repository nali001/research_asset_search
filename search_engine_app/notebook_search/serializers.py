
# serializers.py
''' Define the serializers for specific models
'''

from rest_framework import serializers

# from notebook_search.models import GithubNotebookResult
# # from notebook_search.models import NotebookSearchRequest
# from notebook_search.models import NotebookSearchRequestLog
# from notebook_search.models import ClientUser
from notebook_search.models import UserProfile
from notebook_search.models import NotebookSearchLog
from notebook_search.models import KaggleNotebook






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
        # Modify the fields to get a subset of fields to serialize
        fields = '__all__'


class KaggleNotebookResultSerializer(serializers.ModelSerializer):
    ''' A nested serliazer for generating responses for notebook search using Kaggle notebooks

    It copys the notebook search request information received from the client and adds a list of notebook results
    '''
    notebook_results = KaggleNotebookSerializer(many=True)
    class Meta:
        model = NotebookSearchLog
        # Modify the fields to get a subset of fields to serialize
        fields = '__all__'

# -----------------------------------------------------------------


# # ------------------- Query generation serializers --------------------
# class QueryGenerationSession(): 
#     ''' Query generation session
#     '''
# # -----------------------------------------------------------------




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
