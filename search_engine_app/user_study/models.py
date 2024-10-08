from django.db import models

class Participant(models.Model):
    # Define your fields here
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    session_id = models.CharField(max_length=100)
    register_time = models.DateTimeField(auto_now_add=True)

    # Add more fields as needed

    def __str__(self):
        return f"{self.session_id}" 





