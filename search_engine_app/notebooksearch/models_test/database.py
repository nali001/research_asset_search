from django.db import models
class NotebookProfile(models.Model): 

    pass

class UserProfile(models.Model): 
    ''' User profile 
    '''
    research_interests = models.TextField()


class QueryProfile(models.Model): 
    ''' Abstract query model that contains minimum set of query attributes
    '''