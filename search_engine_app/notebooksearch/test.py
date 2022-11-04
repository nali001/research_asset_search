from notebooksearch import query_generation
from pprint import pprint

# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health." 

# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

query_generator = query_generation.QueryGenerator(doc_set)
# corpus_tokens = query_generator.get_corpus_tokens()
# print(corpus_tokens)

# vocab = query_generator.get_vocab()
# # print(vocab)

# query = vocab[0]
# print(query)

# doc_scores = query_generation.QueryGenerator.bm25_ranking(query, corpus_tokens)
vocab_ranks = query_generator.get_vocab_ranks()
pprint(vocab_ranks)
