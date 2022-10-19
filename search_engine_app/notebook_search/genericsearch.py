# genericsearch.py
'''' This module retrieves notebooks from indexes
'''
import numpy as np
from spellchecker import SpellChecker
import requests
from bs4 import BeautifulSoup

#-----------------------------------------------------------------------------------------------------------------------
def synonyms(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})]
#-----------------------------------------------------------------------------------------------------------------------

class Genericsearch():
    ''' Provide an entrypoint for generic notebook search
    '''
    def __init__(self, request, es, index_name): 
        self.request = request
        self.es = es
        self.index_name = index_name
        self.response_data = {}

    def genericsearch(self):
        ''' Provide retrival functionality towards an Elasticsearch index of given index_name. 
        '''
        request = self.request
        es = self.es
        index_name = self.index_name

        # # Create index from Jupyter notebooks 
        # if not es.indices.exists(index = index_name): 
        #     github_notebook_path = os.path.join(os.getcwd(), 'notebook_search', 'Github Notebooks')
        #     indexer = ElasticsearchIndexer(es, "Github", "github_notebooks", github_notebook_path)
        #     # kaggle_notebook_path = os.path.join(os.getcwd(), 'notebook_search', 'Kaggle Notebooks')
        #     # indexer = ElasticsearchNotebookIndexer(es, "Kaggle", "kaggle_notebooks", kaggle_notebook_path)
        #     indexer.index_notebooks()
        
        try:
            term = request.GET['term']
        except:
            term = ''
        if (term=="*"):
            term=""
        try:
            term = request.GET['term']
            term=term.rstrip()
            term=term.lstrip()
        except:
            term = ''

        try:
            page = request.GET['page']
        except:
            page = 0

        try:
            filter = request.GET['filter']
        except:
            filter = ''

        try:
            facet = request.GET['facet']
        except:
            facet = ''

        try:
            suggestedSearchTerm = request.GET['suggestedSearchTerm']
        except:
            suggestedSearchTerm = ''

        
        print("TERMMMMMMM: \n", term)
        searchResults = self.getSearchResults(request, facet, filter, page, term)

        if(suggestedSearchTerm != ""):
            searchResults["suggestedSearchTerm"]=""
        else:
            suggestedSearchTerm=""
            if searchResults["NumberOfHits"]==0:
                suggestedSearchTerm= self.potentialSearchTerm(term)
                searchResults=self.getSearchResults(request, facet, filter, page, "*")
                searchResults["NumberOfHits"]=0
                searchResults["searchTerm"]=term
                searchResults["suggestedSearchTerm"]=suggestedSearchTerm
        return searchResults

  
    # def return_notebook_results(self): 
    #     ''' Generate notebook search results for API endpoint. 
        
    #     Iterate the search results and for each result create a new models.NotebookResultSerializer object.
    #     '''
    #     searchResults = self.genericsearch()
    #     results = []
    #     for item in searchResults['results']: 
    #         results.append(serializers.KaggleNotebookResultSerializer(item).data)
    #         # results.append(serializers.GithubNotebookResultSerializer(item).data)
    #     return results

    def potentialSearchTerm(self, term):
        ''' Get potential search terms
        '''
        alternativeSearchTerm=""

        spell = SpellChecker()
        searchTerm=term.split()
        alternativeSearchTerm=""
        for sTerm in searchTerm:
            alterWord=spell.correction(sTerm)
            if(alterWord!=""):
                alternativeSearchTerm= alternativeSearchTerm+" "+alterWord

        alternativeSearchTerm=alternativeSearchTerm.rstrip()
        alternativeSearchTerm=alternativeSearchTerm.lstrip()

        if alternativeSearchTerm==term:
            alternativeSearchTerm=""
            for sTerm in searchTerm:
                syn=synonyms(sTerm)
                if len(syn)>0:
                    alterWord=syn[0]
                    alternativeSearchTerm= alternativeSearchTerm+" "+alterWord

        alternativeSearchTerm=alternativeSearchTerm.rstrip()
        alternativeSearchTerm=alternativeSearchTerm.lstrip()

        return alternativeSearchTerm
    

    def getSearchResults(self, request, facet, filter, page, term):
        ''' Get search results 
        '''
        es = self.es
        index_name = self.index_name
        if filter!="" and facet!="":
            saved_list = request.session['filters']
            saved_list.append({"term": {facet+".keyword": filter}})
            request.session['filters'] = saved_list
        else:
            if 'filters' in request.session:
                del request.session['filters']
            request.session['filters']=[]

        page=(int(page)-1)*10
        result={}
        if term=="*" or term=="top10":
            result = es.search(
                index=index_name,
                body={
                    "from" : page,
                    "size" : 10,
                    "query": {
                        "bool" : {
                            "must" : {
                                "match_all": {}
                            }
                        }
                    }
                }
            )
        else:
            user_request = "some_param"
            query_body = {
                "from" : page,
                "size" : 10,
                "query": {
                    "bool": {
                        "must": {
                            "multi_match" : {
                                "query": term,
                                "fields": [ "name", "description"],
                                "type": "best_fields",
                                "minimum_should_match": "50%"
                            }
                        },
                    }
                }
            }

            result = es.search(index=index_name, body=query_body)
        lstResults=[]


        for searchResult in result['hits']['hits']:
            lstResults.append(searchResult['_source'])

        numHits=result['hits']['total']['value']

        upperBoundPage=round(np.ceil(numHits/10)+1)
        if(upperBoundPage>10):
            upperBoundPage=11

        facets=[]

        results={
            "facets":facets,
            "results":lstResults,
            "NumberOfHits": numHits,
            "page_range": upperBoundPage,
            "cur_page": (page/10+1),
            "searchTerm":term,
            "functionList": self.getAllfunctionList(request)
        }

        return results


    def getAllfunctionList(self, request):
        ''' Get notebook search results
        '''
        if not 'BasketURLs' in request.session or not request.session['BasketURLs']:
            request.session['BasketURLs'] = []
        if not 'MyBasket' in request.session or not request.session['MyBasket']:
            request.session['MyBasket'] = []

        functionList=""
        saved_list = request.session['MyBasket']
        for item in saved_list:
            functionList= functionList+r"modifyCart({'operation':'add','type':'"+item['type']+"','title':'"+item['title']+"','url':'"+item['url']+"','id':'"+item['id']+"' });"
        return functionList


#-----------------------------------------------------------------------------------------------------------------------
