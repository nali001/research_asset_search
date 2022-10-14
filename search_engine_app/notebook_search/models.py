from django.db import models

# 1. Define the variables for the results. 
# searchResults schema: ['facets', 'results', 'NumberOfHits', 'page_range', 'cur_page', 'searchTerm', 'functionList', 'suggestedSearchTerm']
# result schema: ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']
# ------------------------- Notebook models -----------------------
class BaseNotebook(models.Model): 
    ''' Abstract notebook model that contains minimum set of notebook attributes
    '''
    notebook_id = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    description = models.TextField(default = 'No description.')
    html_url = models.CharField(max_length=240, default = 'No html URL.')
    download_url = models.CharField(max_length=240, default = 'No download URL.')
    class Meta:
        abstract = True

class GithubNotebookResult(BaseNotebook):
    ''' Notebook result specific to Github source
    '''
    full_name = models.CharField(max_length=60)
    stargazers_count = models.IntegerField()
    forks_count = models.IntegerField()
    size = models.IntegerField()
    language = models.CharField(max_length=60)
    git_url = models.CharField(max_length=200)
    class Meta: 
        managed = False
    

class KaggleNotebookResult(BaseNotebook): 
    ''' Notebook result specific to Kaggle source'''
    title = models.CharField(max_length=120)
    kaggle_id = models.CharField(max_length=60)
    file_name = models.CharField(max_length=60)
    class Meta: 
        managed = False

# -----------------------------------------------------------------


# ------------------------- User models -----------------------
class BaseUser(models.Model): 
    ''' Abstract user model that contains minimum set of user attributes
    '''
    user_id = models.CharField(max_length=60)

    class Meta:
        abstract = True


class UserProfile(BaseUser): 
    ''' User profile 
    '''
    research_interests = models.TextField()
# -----------------------------------------------------------------


# ------------------------- Query models -----------------------
class BaseQuery(models.Model): 
    ''' Abstract query model that contains minimum set of query attributes
    '''
    query_id = models.CharField(max_length=60)
    query_text = models.TextField(default = 'unknown')
    
    class Meta:
        abstract = True

class QueryProfile(BaseQuery): 
    ''' Abstract query model that contains minimum set of query attributes
    '''
# -----------------------------------------------------------------

# ------------------------- Cell content models -----------------------
class BaseCellContent(models.Model): 
    ''' Abstract cell content model that contains minimum set of cell attributes
    '''
    # query_id = models.CharField(max_length=60)
    cell_type_choices = [
        ("markdown", "markdown"),
        ("code", "code"), 
        ]
    cell_type = models.CharField(choices = cell_type_choices, max_length=60)
    cell_content = models.TextField()
    def __str__(self): 
        return self.cell_content
    
    class Meta:
        abstract = True
# -----------------------------------------------------------------


# ------------------- Notebook search models --------------------
class NotebookSearchRequest(models.Model): 
    ''' Basic search session
    '''
    user_id = models.CharField(max_length=240, default = 'unknown')
    timestamp = models.DateTimeField(), 
    # event_choices = [
    #     ('notebook_search', 'notebook_search'), 
    #     ('query_generation', 'query_generation'),
    #     ('context_based_search', 'context_based_search'), 
    #     ]
    event = models.CharField(max_length=60, default = 'notebook_search')
    query = models.TextField(default = 'unknown')
    # class Meta:
    #     abstract = True


class NotebookSearchRequest(models.Model): 
    ''' Basic search session
    '''
    user_id = models.CharField(max_length=240, default = 'unknown')
    timestamp = models.CharField(max_length=60, default = 'unknown')
    # event_choices = [
    #     ('notebook_search', 'notebook_search'), 
    #     ('query_generation', 'query_generation'),
    #     ('context_based_search', 'context_based_search'), 
    #     ]
    event = models.CharField(max_length=60, default = 'notebook_search')
    query = models.TextField(default = 'unknown')

    def __str__(self): 
        return self.user_id
    # class Meta:
    #     abstract = True

    
class NotebookSearchRequestLog(models.Model): 
    ''' Basic search session
    '''
    user_id = models.CharField(max_length=240, default = 'unknown')
    timestamp = models.DateTimeField(auto_now=False)
    # event_choices = [
    #     ('notebook_search', 'notebook_search'), 
    #     ('query_generation', 'query_generation'),
    #     ('context_based_search', 'context_based_search'), 
    #     ]
    event = models.CharField(max_length=60, default = 'notebook_search')
    query = models.TextField(default = 'unknown')

    def __str__(self): 
        return self.user_id
    # class Meta:
    #     abstract = True

    

# class NotebookSearchRequest(UserRequest): 
#     ''' Notebook search request
#     '''
#     event = 'notebook_search'
# # class NotebookSearchResponse(): 
# #     ''' Notebook search response
# #     '''
# #     notebook_results = 

# class NotebookSearchLog(UserRequest): 
#     ''' Notebook search session
#     '''


# # -----------------------------------------------------------------

# # ------------------- Query generation models --------------------
# class QueryGenerationSession(): 
#     ''' Query generation session
#     '''
# # -----------------------------------------------------------------


# # ------------------- Context-based search models --------------------
# class ContextSearchSession(BaseUser): 
#     ''' Context-based search session
#     '''



# # -----------------------------------------------------------------

# # ------------------- Relevancy feedback models --------------------
# class RelevancyFeedbackRequest(NotebookSearchRequest): 
#     num_stars = models.IntegerField()

# # class RelevancyFeedbackLog(NotebookSearchRequest, BaseNotebook): 
# #     num_stars = models.IntegerField()
# # -----------------------------------------------------------------


