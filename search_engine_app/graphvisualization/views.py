# graphvisualization/views.py
# Only used for rendering HTML
from django.shortcuts import render
from .models import Node, Edge


def graph_visualization_view(request):
    nodes = Node.objects.all()
    edges = Edge.objects.all()
    return render(request, 'graph_results.html', {'nodes': nodes, 'edges': edges})

 