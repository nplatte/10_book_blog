from django.forms import ModelForm
from django import forms
from posts.models import Post

class PostModelForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'book_author', 'book_title', 'post']
        widgets = {
            'book_author': forms.TextInput(attrs={'id': 'author_entry'}),
            'title': forms.TextInput(attrs={'id': 'title_entry'}),
            'post': forms.Textarea(attrs={'id': 'post_entry'}),
            'book_title': forms.TextInput(attrs={'id': 'book_title_entry'})
        }
