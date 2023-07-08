from django.db import models

class Post(models.Model):
    
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    post = models.TextField()

    def __str__(self):
        return self.title
    

class Tag(models.Model):

    pass
