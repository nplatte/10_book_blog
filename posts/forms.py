from django.forms import ModelForm
from django import forms
from posts.models import Post, Tag
from django.core.exceptions import ValidationError

class PostModelForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'book_author', 'book_title', 'post']
        tags = forms.Textarea()
        widgets = {
            'book_author': forms.TextInput(attrs={'id': 'author_entry'}),
            'title': forms.TextInput(attrs={'id': 'title_entry'}),
            'post': forms.Textarea(attrs={'id': 'post_entry'}),
            'book_title': forms.TextInput(attrs={'id': 'book_title_entry'}),
        }


class TagForm(forms.Form):

    tag_list = forms.CharField(
        max_length=60, 
        widget=forms.Textarea(attrs={'id': 'tag_entry'})
        )
    
    def clean_tag_list(self):
        data = self.cleaned_data['tag_list']
        for tag in data.split(' '):
            if tag[0] != '#':
                raise ValidationError('# missing in tag')
        return data