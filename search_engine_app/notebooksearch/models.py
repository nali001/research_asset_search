from tkinter import CASCADE
from django.db import models

# ------------------------- User models -----------------------
class ClientUser(models.Model): 
    ''' Abstract user model that contains minimum set of user attributes
    '''
    # The ID assigned to a user by the frontend. 
    client_id = models.CharField(max_length=240)

    class Meta:
        abstract = True
    # def __str__(self):
    #     return self.client_id


class UserProfile(ClientUser): 
    ''' User profile 
    '''
    # client_id = models.CharField(max_length=240)
    # client_user = models.ForeignKey(ClientUser, related_name="userprofiles", on_delete=models.CASCADE)
    research_interests = models.TextField()
    def __str__(self):
        return self.client_id
# -----------------------------------------------------------------


# ------------------------- Query models -----------------------
# class Query(models.Model): 
#     ''' Abstract query model that contains minimum set of query attributes
#     '''
#     # query_id = models.CharField(max_length=60)
#     query_text = models.TextField()
    
    # class Meta:
    #     abstract = True

# # class QueryProfile(Query): 
# #     ''' Abstract query model that contains minimum set of query attributes
# #     '''
# # -----------------------------------------------------------------


# ------------------------- Notebook result models -----------------------
class BaseNotebook(models.Model): 
    ''' Abstract notebook model that contains minimum set of notebook attributes
    '''
    name = models.CharField(max_length=60)
    description = models.TextField(default = 'No description.')
    html_url = models.CharField(max_length=240, default = 'No html URL.')
    # download_url = models.CharField(max_length=240, default = 'No download URL.')
    class Meta:
        abstract = True

# class GithubNotebookResult(BaseNotebook):
#     ''' Notebook result specific to Github source
#     '''
    # notebook_id = models.CharField(max_length=60)
# 
#     full_name = models.CharField(max_length=60)
#     stargazers_count = models.IntegerField()
#     forks_count = models.IntegerField()
#     size = models.IntegerField()
#     language = models.CharField(max_length=60)
#     git_url = models.CharField(max_length=200)
#     class Meta: 
#         managed = False
    
# -----------------------------------------------------------------



# # ------------------------- Cell content models -----------------------
# class BaseCellContent(models.Model): 
#     ''' Abstract cell content model that contains minimum set of cell attributes
#     '''
#     # query_id = models.CharField(max_length=60)
#     cell_type_choices = [
#         ("markdown", "markdown"),
#         ("code", "code"), 
#         ]
#     cell_type = models.CharField(choices = cell_type_choices, max_length=60)
#     cell_content = models.TextField()
#     def __str__(self): 
#         return self.cell_content
    
#     class Meta:
#         abstract = True
# # -----------------------------------------------------------------


# ------------------- Notebook search models --------------------    
class NotebookSearchLog(ClientUser): 
    ''' Basic notebook search request
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


