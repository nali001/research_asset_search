# ir/ner.py

class EntityExtractor:
    def __init__(self, content_type=None, model_name=None):
        self.content_type = content_type
        self.model_name = model_name
        self.models = {
            "xxx": self._xxx,  # Placeholder for entity extraction function
        }

    def extract_entities(self, content):
        if self.model_name not in self.models:
            raise ValueError("Model not supported.")
        extraction_function = self.models[self.model_name]
        entities = extraction_function(content)
        return entities

    def _xxx(self, content):
        # Placeholder for entity extraction function
        # Replace this with your actual entity extraction logic
        # For now, just splitting the content into words and returning them as entities
        toy_entities = {
            "task": "Data Wrangling",
            "dataset": "Turbofan Engine Degradation Simulation Data Set",
            "method": "Importing txt files and consolidating data into csv files"
        }
        return toy_entities
