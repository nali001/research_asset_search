# graphvisualization.serializers.py
# serializers.py
from rest_framework import serializers
from .models import GraphData

class GraphNodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField()

class GraphEdgeSerializer(serializers.Serializer):
    from_node = serializers.IntegerField(source='source')
    to_node = serializers.IntegerField(source='target')

class GraphDataSerializer(serializers.ModelSerializer):
    nodes = GraphNodeSerializer(many=True)
    edges = GraphEdgeSerializer(many=True)

    class Meta:
        model = GraphData
        fields = ('nodes', 'edges')
