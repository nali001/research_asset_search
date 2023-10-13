import os
import json
from haystack.nodes import JsonConverter, PreProcessor, EmbeddingRetriever
from haystack.document_stores import FAISSDocumentStore

class FaissDenseIndexer:
    def __init__(self, notebook_dir, docs_file, faiss_index_dir, faiss_db_dir, embedding_model):
        self.notebook_dir = notebook_dir
        self.docs_file = docs_file
        self.faiss_index_dir = faiss_index_dir
        self.faiss_db_dir = faiss_db_dir
        self.embedding_model = embedding_model
        self.document_store = None

    def extract_data_from_json(self):
        data = []
        for filename in os.listdir(self.notebook_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.notebook_dir, filename)
                with open(file_path, "r") as f:
                    json_data = json.load(f)
                    data.append({
                        "docid": json_data["docid"],
                        "content": json_data["description"],
                    })
        return data

    def preprocess_data(self, data):
        converter = JsonConverter()
        docs = converter.convert(self.docs_file)

        processor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=True,
            split_by="word",
            split_length=512,
            split_respect_sentence_boundary=True,
            split_overlap=0
        )

        passages = processor.process(docs)
        return passages

    def index_documents(self, passages):
        os.makedirs(f"{self.faiss_db_dir}/{self.embedding_model[0]}", exist_ok=True)
        document_store = FAISSDocumentStore(sql_url=f"sqlite:///{self.faiss_db_dir}/{self.embedding_model[0]}/faiss_base.db", faiss_index_factory_str="Flat")

        for i, passage in enumerate(passages):
            docid = passage.meta['docid']
            passage_docid = f"{docid}_passage{i}"
            index_document = {
                "id": passage_docid,
                "content": passage.content,
                "meta": {
                    "name": docid,
                    "passage_number": i,
                },
            }
            document_store.write_documents([index_document])

        self.document_store = document_store
        return document_store

    def update_index(self):
        retriever = EmbeddingRetriever(
            document_store=self.document_store,
            embedding_model=self.embedding_model[1],
        )

        self.document_store.update_embeddings(retriever)

        index_path = f"{self.faiss_index_dir}/{self.embedding_model[0]}/index.faiss"
        config_path = f"{self.faiss_index_dir}/{self.embedding_model[0]}/config.json"
        os.makedirs(f"{self.faiss_index_dir}/{self.embedding_model[0]}", exist_ok=True)

        self.document_store.save(index_path=index_path, config_path=config_path)
        print(f"Save index to {index_path}")

    def load_index(self):
        index_path = f"{self.faiss_index_dir}/{self.embedding_model[0]}/index.faiss"
        config_path = f"{self.faiss_index_dir}/{self.embedding_model[0]}/config.json"
        self.document_store = FAISSDocumentStore.load(index_path=index_path, config_path=config_path)
        assert self.document_store.faiss_index_factory_str == "Flat"

def dense_index_preprocessed_notebooks(source_name=None): 
    notebook_dir = f'./data/notebook/{source_name}/preprocessed_content/notebooks_summaries'
    docs_file = '../preprocessed_data/docs.json'
    faiss_index_dir = './faiss_indexes_512'
    faiss_db_dir = './faiss_db_512'
    embedding_models = [("model1", "sentence-transformers/multi-qa-mpnet-base-dot-v1"),
                        ("model2", "sentence-transformers/all-mpnet-base-v2")]

    embedding_model = embedding_models[1]

    dense_indexer = FaissDenseIndexer(notebook_dir, docs_file, faiss_index_dir, faiss_db_dir, embedding_model)

    data = dense_indexer.extract_data_from_json()
    passages = dense_indexer.preprocess_data(data)
    document_store = dense_indexer.index_documents(passages)
    dense_indexer.update_index()


def main(): 
    dense_index_preprocessed_notebooks(source_name='Kaggle')

if __name__ == '__main__': 
    ''' python -m dense_indexer.faiss_indexing_512'''
    main()