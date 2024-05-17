# graphvisualization/views.py
# Only used for rendering HTML
from django.shortcuts import render

from .generate_graph import GraphGenerator


def graph_visualization_view(request):
    query_data = request.GET
    graph_path = "../data/KG/PWC/datasets_kg.graphml" 
    graph_generator = GraphGenerator(graph_path=graph_path)
    print(query_data)

    keyword = query_data['query']
    max_distance = int(query_data['distance'])
    graph = graph_generator.search_graph(keyword=keyword, mode='label', max_distance=max_distance)
    
    result = {"graph": graph}
    return render(request, 'graph_results.html', result)


 