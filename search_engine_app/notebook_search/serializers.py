
# serializers.py
''' Define the serializers for specific models
'''

from rest_framework import serializers

# from notebook_search.models import GithubNotebookResult
# from notebook_search.models import KaggleNotebookResult
# # from notebook_search.models import NotebookSearchRequest
# from notebook_search.models import NotebookSearchRequest
# from notebook_search.models import NotebookSearchRequestLog
# from notebook_search.models import ClientUser
from notebook_search.models import UserProfile




# class GithubNotebookResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GithubNotebookResult
#         # Modify the fields to get a subset of fields to serialize
#         fields = ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']


# class KaggleNotebookResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KaggleNotebookResult
#         # Modify the fields to get a subset of fields to serialize
#         fields = ['kaggle_id', 'name', 'file_name', 'description', 'html_url']

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
    ''' A nested serializer for serializing UserProfile data
    '''
    # client_user = serializers.SlugRelatedField(
    #     many=True, 
    #     read_only=False, 
    #     slug_field= "client_id", 
    #     queryset=ClientUser.objects.all()
    # )
    class Meta: 
        model = UserProfile
        fields = '__all__'