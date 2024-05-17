import json
import networkx as nx

class KnowledgeGraphConstructor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.graph = nx.Graph()
        self.label_to_id = {}  # Mapping from label to node ID

    def generate_id(self, label):
        if label in self.label_to_id:
            return self.label_to_id[label]

        # Generate a new ID if the label doesn't exist
        counter = 1
        while f"{label}_{counter}" in self.label_to_id.values():
            counter += 1

        node_id = f"{label}_{counter}"
        self.label_to_id[label] = node_id
        return node_id

    def build_PWC_KG(self):
        # Load the JSON data from the input file
        with open(self.input_path, 'r') as json_file:
            data = json.load(json_file)

        # Iterate through the datasets and build nodes for dataset name and task
        # Iterate through the datasets and build nodes for dataset name and task
        for dataset in data:
            dataset_name = dataset.get('name')
            task = dataset.get('tasks', [])[0].get('task') if dataset.get('tasks') else None

            if dataset_name:
                dataset_id = self.generate_id(dataset_name)
                self.graph.add_node(dataset_id, label=dataset_name, type="dataset")
            if task:
                task_id = self.generate_id(task)
                self.graph.add_node(task_id, label=task, type="task")

            # Add an edge between dataset name and task
            if dataset_name and task:
                self.graph.add_edge(dataset_id, task_id)


    def save_graph(self, format="graphml"):
        if format == "graphml":
            nx.write_graphml(self.graph, self.output_path)
            print("Knowledge graph saved in GraphML format:", output_path)
        # Add other formats as needed

if __name__ == '__main__':
    # Sample input path to the JSON data
    ''' python -m graphvisualization.build_kg
    '''
    input_path = "../data/KG/PWC/datasets.json" 
    output_path = "../data/KG/PWC/datasets_kg.graphml" 

    # Create a KnowledgeGraphConstructor instance and build the knowledge graph
    kg_constructor = KnowledgeGraphConstructor(input_path, output_path)
    kg_constructor.build_PWC_KG()

    # Save the graph in GraphML format
    kg_constructor.save_graph()

