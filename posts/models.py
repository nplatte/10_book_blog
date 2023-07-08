from django.db import models


class Tag(models.Model):

    tag_name = models.CharField(max_length=15)

    def __str__(self):
        return self.tag_name
    

class Post(models.Model):
    
    title = models.CharField(max_length=20)
    book_author = models.CharField(max_length=20)
    book_title = models.CharField(max_length=30)
    post = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title