from django.db import models

class GraphData(models.Model):
    graph_json = models.TextField()
