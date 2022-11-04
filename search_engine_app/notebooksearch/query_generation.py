import pandas as pd
import numpy as np

from gensim.parsing.preprocessing import remove_stopwords
from gensim.utils import tokenize
from rank_bm25 import BM25Okapi
from rake_nltk import Rake


class QueryGenerator:
    ''' A class for generating all kinds of '''
    def __init__(self, doc_set): 
        self.doc_set = doc_set
        self.corpus_tokens = None
        self.corpus = None
        self.vocab = None
        
    @classmethod
    def tokenize_text(cls, text): 
        ''' Tokenize the text. 
        
        Here we use `gensim` to remove stopwords and tokenize text. 
        The gensim tokenizer does NOT treat punctuation as tokens. 
        Steps: 
            - Lower case
            - Remove stop words
            - Tokenize each document
        '''
        text = text.lower()
        filtered_text = remove_stopwords(text)
        tokenized_text = list(tokenize(filtered_text))
        return tokenized_text

    @classmethod
    def generate_vocab(cls, texts): 
        ''' Get vocabulary from a list of tokenized documents
        '''
        all_words = []
        for text in texts: 
            tokens = text.split(' ')
            all_words.extend(tokens)
        vocab = list(set(all_words))
        return vocab
        
    @classmethod
    def bm25_ranking(cls, query, corpus_tokens): 
        ''' Compute the BM25 scores for all the words in one document

        Using rank-bm25 library: https://github.com/dorianbrown/rank_bm25 
        '''

        bm25 = BM25Okapi(corpus_tokens)
        tokenized_query = QueryGenerator.tokenize_text(query)
        doc_scores = bm25.get_scores(tokenized_query)
        return doc_scores

    @classmethod
    def extract_keywords_rake(cls, text): 
        ''' Extract keywords from a piece of text using RAKE (Rapid Automatic Keyword Extraction) algorithm

        Here we use `rake-nltk` library https://github.com/csurfer/rake-nltk
        '''

        # Uses stopwords for english from NLTK, and all puntuation characters by
        # default
        r = Rake()
        # Extraction given the text.
        r.extract_keywords_from_text(text)

        # To get keyword phrases ranked highest to lowest with scores.
        return r.get_ranked_phrases_with_scores()


    def __prepare_corpus(self): 
        ''' Preprocessing corpus by tokenize all the documents. 
        '''
        doc_set = self.doc_set
        corpus_tokens = []
        corpus = []
        for doc in doc_set: 
            tokenized_doc = QueryGenerator.tokenize_text(doc)
            corpus_tokens.append(tokenized_doc)
            corpus.append(' '.join(tokenized_doc))
        self.corpus_tokens = corpus_tokens
        self.corpus = corpus

    def __generate_vocab(self): 
        ''' Get vocabulary from a list of tokenized documents
        '''
        if self.corpus == None: 
            self.__prepare_corpus()
        texts = self.corpus
        vocab = QueryGenerator.generate_vocab(texts)
        self.vocab = vocab

    def get_corpus(self): 
        if self.corpus == None: 
            self.__prepare_corpus()
        return self.corpus

    def get_corpus_tokens(self): 
        if self.corpus == None: 
            self.__prepare_corpus()
        return self.corpus_tokens

    def get_vocab(self): 
        if self.vocab == None: 
            self.__generate_vocab()
        return self.vocab
        
    
    def get_vocab_bm25_scores(self): 
        ''' Rank the words in a collection of articles based on the importance of the word

        Returns: 
            - Top `num_words` words according to the important ranking. 

        '''
        # Compute BM25 scores for each word in the vocabulary
        if self.corpus_tokens == None: 
            self.__prepare_corpus()
        if self.vocab == None: 
            self.__generate_vocab()

        corpus_tokens = self.corpus_tokens
        vocab = self.vocab

        word_doc_scores = []
        # print(vocab)
        for query in vocab: 
            doc_scores = list(QueryGenerator.bm25_ranking(query, corpus_tokens))
            doc_scores.sort(reverse=True)

            # We only consider the first 100 documents
            word_doc_scores.append(doc_scores[:100])
        return word_doc_scores

    def get_vocab_ranks(self): 
        df_vocab_rank = pd.DataFrame()
        df_vocab_rank['vocab'] = self.get_vocab()
        vocab_scores = self.get_vocab_bm25_scores()

        # Compute average BM25 socres of all the documents. 
        vocab_scores = np.array(vocab_scores)
        df_vocab_rank['avg_BM25'] = np.mean(vocab_scores, axis=1)
        df_vocab_rank.sort_values(by='avg_BM25', ascending=False, inplace=True)
        return df_vocab_rank

    
    def get_keywords(self): 
        pass

    


