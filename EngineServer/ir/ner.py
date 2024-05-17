# ir/ner.py
import openai
import os


class EntityExtractor:
    def __init__(self, content_type=None, model_name=None):
        self.content_type = content_type
        self.model_name = model_name
        self.models = {
            "chatgpt": self._chatgpt,  # Placeholder for entity extraction function
        }

    def extract_entities(self, content):
        if self.model_name not in self.models:
            raise ValueError("Model not supported.")
        extraction_function = self.models[self.model_name]
        entities = extraction_function(content)
        return entities
    


    def _chatgpt(self, content):
        print(os.getcwd())
        with open('../secrets/openai_token.txt', 'r') as f: 
            api_key = f.read()
            openai.api_key = api_key

        if type(content) != str:
            raise ValueError("Content must be a string.")
        
        # Define a list of messages as input for the chat model
        messages = [
            {"role": "system", "content": "Extract task, dataset and method entities from the text. Output the entities in a Json format using these keys: {'task', 'dataset', 'method'}"},
            {"role": "user", "content": content},
        ]

        # Use the OpenAI API for chat completions
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125", # "gpt-3.5-turbo",  # Use the appropriate model
            messages=messages,
            max_tokens=1240,  # Adjust as needed
            temperature=0.3,  # Lower temperature for more deterministic output

        )
        
        breakpoint()

        # Extract the assistant's reply from the response
        entities = response.choices[0].message.content
        return entities

