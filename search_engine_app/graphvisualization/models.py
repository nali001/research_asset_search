from django.db import models

class Node(models.Model):
    name = models.CharField(max_length=100)

class Edge(models.Model):
    source = models.ForeignKey(Node, related_name='outgoing_edges', on_delete=models.CASCADE)
    target = models.ForeignKey(Node, related_name='incoming_edges', on_delete=models.CASCADE)
