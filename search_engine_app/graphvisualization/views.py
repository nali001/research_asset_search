# graphvisualization/views.py
# Only used for rendering HTML
from django.shortcuts import render

from .generate_graph import GraphGenerator


def graph_visualization_view(request):
    graph_path = "../data/KG/PWC/datasets_kg.graphml" 
    graph_generator = GraphGenerator(graph_path=graph_path)
    graph = graph_generator.search_graph(keyword='mnist', mode='label', max_distance=2)
    
    result = {"graph": graph}
    return render(request, 'graph_results.html', result)


 