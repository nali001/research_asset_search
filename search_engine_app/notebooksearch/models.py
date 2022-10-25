from tkinter import CASCADE
from django.db import models
from django.contrib.postgres.fields import ArrayField

# ------------------------- User models -----------------------
class BaseUser(models.Model): 
    ''' Abstract user model that contains minimum set of user attributes
    '''
    # The ID assigned to a user by the frontend. 
    client_id = models.CharField(max_length=240)

    class Meta:
        abstract = True
    # def __str__(self):
    #     return self.client_id


class UserProfile(BaseUser): 
    ''' User profile 
    '''
    # client_id = models.CharField(max_length=240)
    # client_user = models.ForeignKey(ClientUser, related_name="userprofiles", on_delete=models.CASCADE)
    research_interests = models.TextField()
    def __str__(self):
        return self.client_id
# -----------------------------------------------------------------

# ------------------- Notebook search models --------------------    
class BaseNotebook(models.Model): 
    ''' Abstract notebook model that contains minimum set of notebook attributes
    '''
    name = models.CharField(max_length=60)
    description = models.TextField(default = 'No description.')
    html_url = models.CharField(max_length=240, default = 'No html URL.')
    # download_url = models.CharField(max_length=240, default = 'No download URL.')
    class Meta:
        abstract = True

class NotebookSearchParam(models.Model): 
    ''' Model for parameters contained in notebook search requests

    For both `GET` and `POST` mthods
    '''
    page = models.CharField(max_length=60)
    query = models.CharField(max_length=240)
    filter = models.CharField(max_length=60, null=True, blank=True)
    facet = models.CharField(max_length=60, null=True, blank=True)

    class Meta:
        managed = False
    def __str__(self):
        return str(self.query)

class NotebookSearchLog(BaseUser): 
    ''' Model for data contained in notebook search `POST` requests
    '''
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)
    query = models.TextField()
    # class Meta:
    #     abstract = True
    def __str__(self):
        return self.client_id


class NotebookSearchResult(models.Model): 
    ''' notebook_results
    ['query', 'facets', 'num_hits', 'num_pages', 'current_page', 'results']
    '''
    query = models.CharField(max_length=240)
    facets = models.CharField(max_length=60)
    num_hits = models.IntegerField()
    num_pages = models.IntegerField()
    current_page = models.IntegerField()
    # functionList = models.CharField(max_length=60)

    class Meta: 
        managed = False


class KaggleNotebook(BaseNotebook): 
    ''' A notebook result specific to Kaggle source

    ['kaggle_id', 'name', 'file_name', 'html_url', 'description']
    '''
    # title = models.CharField(max_length=120)
    kaggle_id = models.CharField(max_length=60)
    file_name = models.CharField(max_length=60)
    notebook_search_result = models.ForeignKey(NotebookSearchResult, related_name="results", on_delete=models.CASCADE)
    
    class Meta: 
        managed = False
# -----------------------------------------------------------------



# ------------------------- Query models -----------------------
class BaseQuery(models.Model): 
    ''' Abstract query model that contains minimum set of query attributes
    '''
    # query_id = models.CharField(max_length=60)
    query_text = models.TextField()
    # def __str__(self):
    #     return self.query_text
    
    class Meta:
        abstract = True
# -----------------------------------------------------------------


# ------------------------- Query generation models -----------------------
class QueryGenerationLog(BaseUser): 
    ''' Query generation request model
    '''
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)

    class Meta:
        managed = False

    def __str__(self):
        return self.client_id

class CellContent(models.Model): 
    ''' Cell content model 
    '''
    cell_type = models.CharField(max_length=60)
    cell_content = models.TextField()
    query_generation_log = models.ForeignKey(QueryGenerationLog, related_name="cell_contents", on_delete=models.CASCADE)
   
    class Meta:
        managed = False

    def __str__(self): 
        return str(self.id)


class QueryGenerationResult(BaseUser): 
    ''' Query generation result model

    Each query generation method will generate 10 queries. 
    ''' 
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)

    class Meta:
        managed = False

    def __str__(self):
        return self.client_id
        

class GeneratedQuery(models.Model): 
    # generation_method = models.CharField(max_length=60)
    generation_method = models.CharField(max_length=60)
    generated_queries = ArrayField(
        models.CharField(max_length=120, blank=True), 
        size=10,
    )
    class Meta: 
        managed = False
    def __str__(self): 
        return self.generation_method



# class QueryProfile(Query): 
#     ''' Abstract query model that contains minimum set of query attributes
#     '''

# -----------------------------------------------------------------


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


