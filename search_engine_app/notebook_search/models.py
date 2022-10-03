from django.db import models

# 1. Define the variables for the results. 
# searchResults schema: ['facets', 'results', 'NumberOfHits', 'page_range', 'cur_page', 'searchTerm', 'functionList', 'suggestedSearchTerm']
# result schema: ['name', 'full_name', 'stargazers_count', 'forks_count', 'description', 'size', 'language', 'html_url', 'git_url']
class NotebookResultBase(models.Model): 
    name = models.CharField(max_length=60)
    full_name = models.CharField(max_length=60)
    def __str__(self): 
        return self.name

class NotebookResultGithub(NotebookResultBase):
    # name = models.CharField(max_length=60)
    # full_name = models.CharField(max_length=60)
    stargazers_count = models.IntegerField()
    forks_count = models.IntegerField()
    description = models.TextField()
    size = models.IntegerField()
    language = models.CharField(max_length=60)
    html_url = models.CharField(max_length=200)
    git_url = models.CharField(max_length=200)

class NotebookResultKaggle(models.Model): 
    name = models.CharField(max_length=60)
    source = models.CharField(max_length=60)
    full_name = models.CharField(max_length=60)
    stargazers_count = models.IntegerField()
    forks_count = models.IntegerField()
    description = models.TextField()
    size = models.IntegerField()
    language = models.CharField(max_length=60)
    html_url = models.CharField(max_length=200)
    download_url = models.CharField(max_length=200)
    def __str__(self):
        return self.name