from django.db import models

# 1. Define the variables for the results. 
# searchResults schema: ['facets', 'results', 'NumberOfHits', 'page_range', 'cur_page', 'searchTerm', 'functionList', 'suggestedSearchTerm']
# result schema: ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']
# ------------------------- Notebook models -----------------------
class BaseNotebookInfo(models.Model): 
    ''' Basic notebook information 
    '''
    notebook_id = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    description = models.TextField()
    html_url = models.CharField(max_length=240)
    download_url = models.CharField(max_length=240)
    def __str__(self): 
        return self.name

class GithubNotebookResult(BaseNotebookInfo):
    full_name = models.CharField(max_length=60)
    stargazers_count = models.IntegerField()
    forks_count = models.IntegerField()
    size = models.IntegerField()
    language = models.CharField(max_length=60)
    git_url = models.CharField(max_length=200)

class KaggleNotebookResult(BaseNotebookInfo): 
    title = models.CharField(max_length=120)
    kaggle_id = models.CharField(max_length=60)
    file_name = models.CharField(max_length=60)

# -----------------------------------------------------------------


# ------------------------- User models -----------------------
class BaseUserInfo(models.Model): 
    ''' Basic user information
    '''
    user_id = models.CharField(max_length=60)
    def __str__(self): 
        return self.user_id

class UserProfile(BaseUserInfo): 
    ''' User profile 
    '''
    research_interests = models.TextField()
# -----------------------------------------------------------------


# ------------------------- Query models -----------------------
class BaseQuery(models.Model): 
    ''' Basic query info
    '''
    # query_id = models.CharField(max_length=60)
    query_text = models.TextField()
    def __str__(self): 
        return self.query_text
# -----------------------------------------------------------------


# ------------------- User-notebook interaction models --------------------
class BaseSearchRequest(BaseUserInfo): 
    ''' Basic search session
    '''
    event_choices = ['notebook_search', 'query_generation', 'context_based_search']
    event = models.CharField(choices = event_choices, max_length=60)


class QueryGenerationSession(): 
    ''' Query generation session
    '''


class NotebookSearchSession(BaseSearchSession, BaseQuery): 
    ''' Notebook search session
    '''
    description = models.TextField()
    html_url = models.CharField(max_length=60)
    def __str__(self): 
        return self.name

class ContextSearchSession(BaseUserInfo): 
    ''' Context-based search session
    '''


class UserRelevancyRating(UserNotebookSearch): 


# -----------------------------------------------------------------
