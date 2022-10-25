class QueryGenerator:
    def __init__(self, cell_contents):
        self.cell_contents = cell_contents

    def generate_queries(self):
        cell_contents = self.cell_contents
        generated_queries = []
        for cell in cell_contents:
            print(f'CELLLLLLLL: {cell}\n\n')
            lsa_queries = self.lsa(cell["cell_content"])
            queries_by_method = {
                'method': 'LSA', 
                'queries': [lsa_queries]*10
            }
            generated_queries.append(queries_by_method)
        return generated_queries

    def lsa(self, text): 
        processed_text = text
        return processed_text



