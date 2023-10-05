import networkx as nx
import json

class GraphGenerator: 
    def __init__(self, graph_path=None): 
        if graph_path is None: 
            self.G = self._generate_sample_graph()
        else: 
            self.G = self._load_graph(graph_path)

    # Generate a sample graph using NetworkX
    @staticmethod
    def _generate_sample_graph():
        G = nx.Graph()
        G.add_node(1, label="Node 1")
        G.add_node(2, label="Node 2")
        G.add_node(3, label="Node 3")
        G.add_node(4, label="Node 4")
        G.add_edge(1, 2)
        G.add_edge(1, 3)
        G.add_edge(3, 4)
        return G

    @staticmethod
    def _load_graph(graph_path, format="graphml"):
        if format == "graphml":
            print("Knowledge graph loaded from GraphML file:", graph_path)
            return nx.read_graphml(graph_path)
        # Add other formats as needed
    

    def _extract_subgraph(self, nodes_to_match, max_distance):
        """
        Extracts a subgraph induced by the nodes and their neighbors within the specified maximum distance.

        Parameters:
        - graph (NetworkX Graph): The input graph.
        - nodes_to_match (list): A list of nodes for which the subgraph is extracted.
        - max_distance: The maximum distance to include neighbors in the subgraph.

        Returns:
        - subgraph (NetworkX Graph): The subgraph induced by the nodes and their neighbors within the specified distance.
        """

        graph = self.G
        # Create an empty set to store the nodes and their neighbors
        nodes_and_neighbors = set(nodes_to_match)

        # Iterate over each node in the list and find its neighbors within the maximum distance
        for node in nodes_to_match:
            # Calculate shortest paths from the current node to all other nodes
            shortest_paths = nx.single_source_shortest_path_length(graph, node)
            
            # Filter nodes based on distance
            neighbors = [n for n, distance in shortest_paths.items() if distance <= max_distance]
            
            # Add the node and its neighbors to the set
            nodes_and_neighbors.update(neighbors)

        # Extract the subgraph induced by the nodes and their chosen neighbors
        subgraph = graph.subgraph(nodes_and_neighbors)
        return subgraph

    def _match_nodes(self, keyword, mode='label'):
        result_nodes = []
        keyword = keyword.lower()

        for node, data in self.G.nodes(data=True):
            if mode == 'label':
                label = data.get('label', '').lower()
                if keyword in label:
                    result_nodes.append(node)
            elif mode == 'node_id':
                if keyword == str(node):
                    label = data.get('label', '').lower()
                    result_nodes.append(node)
            # Add more modes as needed

        return result_nodes
    
    def search_graph(self, keyword='mnist', mode='label', max_distance=2): 
        ''' Search nodes with keyword and return a subgraph 
        '''
        result_nodes = self._match_nodes(keyword, mode)
        result_subgraph = self._extract_subgraph(result_nodes, max_distance=max_distance)
        graph = self._serialize_graph(result_subgraph)
        return graph

    # Serialize the graph nodes to dict
    @staticmethod
    def _compute_node_size(num_edges):
        # Define the quadratic scaling function, adjust the coefficients based on your requirements
        a = 0  # Coefficient
        b = 0  # Coefficient
        c = 20.0  # Coefficient

        # Scale the node size using a quadratic function
        size = a * num_edges ** 2 + b * num_edges + c
        return size
    
    @staticmethod
    def _serialize_nodes(graph):
        # Define a dictionary to map node types to colors
        NODE_TYPE_COLORS = {
            "dataset": "#40E0D0",
            "task": "#4169E1",
            # Add more mappings as needed
        }

        node_data = [{"id": node, 
                      "label": data.get("label", ""), 
                      "size": GraphGenerator._compute_node_size(graph.degree(node)), 
                      "color": NODE_TYPE_COLORS.get(data.get("type", ""), "gray")
                      } for node, data in graph.nodes(data=True)]
        return {"nodes": node_data}

    # Serialize the graph edges to dict
    @staticmethod
    def _serialize_edges(graph):
        edge_data = [{"from": u, "to": v} for u, v in graph.edges()]
        return {"edges": edge_data}

    @staticmethod
    def _serialize_graph(graph):
        nodes_data = GraphGenerator._serialize_nodes(graph)
        edges_data = GraphGenerator._serialize_edges(graph)
        return {"nodes": nodes_data["nodes"], "edges": edges_data["edges"]}
    
    def get_graph(self): 
        graph = self._serialize_graph(self.G)
        return graph

if __name__ == "__main__":
    ''' python -m graphvisualization.generate_graph
    '''
    graph_path = "../data/KG/PWC/datasets_kg.graphml" 
    graph_generator = GraphGenerator(graph_path=graph_path)
    # graph = graph_generator.get_graph()
    graph = graph_generator.search_graph(keyword='mnist', mode='label', max_distance=2)

    print(graph)
