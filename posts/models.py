from django.db import models

class Post(models.Model):
    
    title = models.CharField(max_length=20)
    book_author = models.CharField(max_length=20)
    book_title = models.CharField(max_length=30)
    post = models.TextField()

    def __str__(self):
        return self.title
    

class Tag(models.Model):

    pass
