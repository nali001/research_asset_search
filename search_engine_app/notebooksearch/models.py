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


class UserProfile(BaseUser): 
    ''' User profile 
    '''
    research_interests = models.TextField()
    def __str__(self):
        return self.client_id
# -----------------------------------------------------------------

# ------------------- Notebook search models --------------------    
class BaseNotebook(models.Model): 
    ''' Abstract notebook model that contains minimum set of notebook attributes

    docid, name, source, html_url, description
    ''' 
    docid = models.CharField(max_length=240)
    name = models.CharField(max_length=60)
    source = models.CharField(max_length=60)
    html_url = models.CharField(max_length=240, default = 'No html URL.')
    description = models.TextField(default = 'No description.')
    # This is unified notebook ID, assigned to each notebook in the database
    # download_url = models.CharField(max_length=240, default = 'No download URL.')
    class Meta:
        abstract = True

class NotebookSearchParam(models.Model): 
    ''' Model for parameters contained in notebook search requests

    For both `GET` and `POST` mthods
    '''
    page = models.CharField(max_length=60)
    query = models.TextField()
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

    def __str__(self):
        return self.client_id


class NotebookSearchResult(models.Model): 
    ''' notebook_results

    Fields: ['query', 'facets', 'num_hits', 'num_pages', 'current_page', 'results']
    The fields defined below are the high-level fields. 
    The `results` field is a list of notebook results and is only defined by serialiers. 
    '''
    query = models.TextField()
    facets = models.CharField(max_length=60)
    num_hits = models.IntegerField()
    num_pages = models.IntegerField()
    current_page = models.IntegerField()
    # functionList = models.CharField(max_length=60)

    class Meta: 
        managed = False


class KaggleNotebook(BaseNotebook): 
    ''' A notebook result specific to Kaggle source

    docid, source_id, name, file_name, source, html_url, description
    '''
    # title = models.CharField(max_length=120)
    source_id = models.CharField(max_length=60)
    file_name = models.CharField(max_length=60)
    language = models.CharField(max_length=60)
    num_cells = models.CharField(max_length=60)
    notebook_search_result = models.ForeignKey(NotebookSearchResult, related_name="results", on_delete=models.CASCADE)
    
    class Meta: 
        managed = False
# -----------------------------------------------------------------




# ------------------- Notebook download models --------------------    
class NotebookDownloadParam(models.Model): 
    ''' Model for parameters contained in notebook download requests

    For both `GET` and `POST` mthods
    '''
    docid = models.CharField(max_length=240)

    class Meta:
        managed = False
    def __str__(self):
        return str(self.docid)

class NotebookDownloadLog(BaseUser): 
    ''' Model for data contained in notebook search `POST` requests
    '''
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)
    docid = models.CharField(max_length=240)

    def __str__(self):
        return self.docid


class NotebookDownloadResult(models.Model): 
    ''' notebook_results
    ['query', 'facets', 'num_hits', 'num_pages', 'current_page', 'results']
    '''
    docid = models.CharField(max_length=240)
    notebook_source_file = models.TextField()
    # functionList = models.CharField(max_length=60)

    class Meta: 
        managed = False

# -----------------------------------------------------------------



# ------------------------- Query models -----------------------
class BaseQuery(models.Model): 
    ''' Abstract query model that contains minimum set of query attributes
    '''
    query_text = models.TextField()

    class Meta:
        abstract = True
# -----------------------------------------------------------------


# ------------------------- Query generation models -----------------------
class QueryGenerationLog(BaseUser): 
    ''' Query generation request model
    '''
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)

    def __str__(self):
        return self.client_id


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
# -----------------------------------------------------------------


# ------------------- Context-based search models --------------------
class ContextSearchLog(BaseUser): 
    ''' Context-based search session
    '''
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)
    query = models.TextField()

    # class Meta:
    #     abstract = True
    def __str__(self):
        return self.client_id


class ContextSearchResult(BaseUser): 
    ''' Query generation result model

    Each query generation method will generate 10 queries. 
    ''' 
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)
    query = models.TextField()

    class Meta:
        managed = False

    def __str__(self):
        return self.client_id
# # -----------------------------------------------------------------


# ------------------- Cell contents models --------------------
class CellContent(models.Model): 
    ''' Cell content model 
    '''
    cell_type = models.CharField(max_length=60)
    cell_content = models.TextField()
    # Add `null=True` to prevent writting to database when no data is passed
    query_generation_log = models.ForeignKey(QueryGenerationLog, null=True, related_name="cell_contents", on_delete=models.CASCADE)
    context_search_log = models.ForeignKey(ContextSearchLog, null=True, related_name="cell_contents", on_delete=models.CASCADE)

    def __str__(self): 
        try: 
            return str(self.query_generation_log.client_id)
        except: 
            return str(self.context_search_log.client_id)
# -----------------------------------------------------------------


# ------------------- Generated query models --------------------
class GeneratedQuery(models.Model): 
    method = models.CharField(max_length=60)
    queries = ArrayField(
        models.CharField(max_length=240, null=True), 
        size=10,
    )
    context_search_log = models.ForeignKey(ContextSearchLog, null=True, related_name="generated_queries", on_delete=models.CASCADE)
    
    def __str__(self): 
        return self.method
# -----------------------------------------------------------------


# ------------------- Relevancy feedback models --------------------
class AnnotatedNotebook(BaseNotebook):
    
    def __str__(self): 
        return str(self.docid)


class RelevancyFeedbackLog(BaseUser): 
    ''' Query generation request model
    '''
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)
    query = models.TextField()
    num_stars = models.CharField(max_length=60)
    annotated_notebook = models.OneToOneField(AnnotatedNotebook, null=True, related_name="RelevancyFeedbackLog", on_delete=models.CASCADE)

    def __str__(self):
        return self.client_id
# -----------------------------------------------------------------


