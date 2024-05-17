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


# ------------------- Dataset search models --------------------    
class BaseDataset(models.Model): 
    ''' Abstract dataset model that contains minimum set of dataset attributes

    ['docid', 'source', 'size', 'name', 'description', 'html_url', 'source_id', 'last_updated', 'license']
    ''' 
    docid = models.CharField(max_length=240)
    source = models.CharField(max_length=60)
    size = models.CharField(max_length=60)
    name = models.CharField(max_length=240)
    description = models.TextField(default = 'No description.')
    html_url = models.CharField(max_length=240, default = 'No HTML URL.')
    source_id = models.CharField(max_length=120, default = 'Unknown')
    last_updated = models.CharField(max_length=60)
    license = models.CharField(max_length=120)

    class Meta:
        abstract = True

class DatasetSearchParam(models.Model): 
    ''' Model for parameters contained in dataset search requests

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

class DatasetSearchLog(BaseUser): 
    ''' Model for data contained in datast search `POST` requests
    '''
    timestamp = models.CharField(max_length=60)
    event = models.CharField(max_length=60)
    query = models.TextField()

    def __str__(self):
        return self.client_id


class DatasetSearchResult(models.Model): 
    ''' dataset_results

    Fields: ['query', 'facets', 'num_hits', 'num_pages', 'current_page', 'results']
    The fields defined below are the high-level fields. 
    The `results` field is a list of dataset results and is only defined by serialiers. 
    '''
    query = models.TextField()
    facets = models.CharField(max_length=60)
    num_hits = models.IntegerField()
    num_pages = models.IntegerField()
    current_page = models.IntegerField()

    class Meta: 
        managed = False


class Dataset(BaseDataset): 
    ''' A dataset result
    '''
    class Meta: 
        managed = False
# -----------------------------------------------------------------


