from django.db import models

# Create your models here.

class Graph(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    roomID = models.IntegerField()

    def _str_(self):
        return self.title