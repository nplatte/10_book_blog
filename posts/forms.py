from django.forms import ModelForm
from posts.models import Post

class PostModelForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'book_author', 'book_title', 'post']
