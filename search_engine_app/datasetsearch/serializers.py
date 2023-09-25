
# serializers.py
''' Define the serializers for specific models
'''

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


from datasetsearch.models import DatasetSearchParam
from datasetsearch.models import DatasetSearchLog
from datasetsearch.models import Dataset
from datasetsearch.models import DatasetSearchResult



# ------------------- Dataset search serializers --------------------    
class DatasetSearchParamSerializer(serializers.ModelSerializer): 
    ''' A serialier for handling parameters of dataset search requests
    '''
    class Meta:
        model = DatasetSearchParam
        fields = '__all__'

class DatasetSearchLogSerializer(serializers.ModelSerializer): 
    ''' A serialier for handling dataset search requests
    '''
    class Meta:
        model = DatasetSearchLog
        fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):
    ''' A serializer for serializing datasets 
    This will be included in DatasetSearchResultSerializer
    '''
    # summarization_scores = SummarizationScoreSerializer(many=True)

    class Meta:
        model = Dataset
        fields = '__all__'


class DatasetSearchResultSerializer(serializers.ModelSerializer):
    ''' A nested serliazer for generating responses for dataset search using datasets

    It copys the dataset search request information received from the client and adds a list of dataset results
    '''
    results = DatasetSerializer(many=True)

    class Meta:
        model = DatasetSearchResult
        fields = '__all__'

# -----------------------------------------------------------------


