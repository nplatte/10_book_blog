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

    general_tag_list = forms.CharField(
        max_length=60, 
        widget=forms.TextInput(attrs={'id': 'general_tag_entry'})
        )
    author_tag_list = forms.CharField(
        max_length=60, 
        widget=forms.TextInput(attrs={'id': 'author_tag_entry'})
        )
    book_tag_list = forms.CharField(
        max_length=60, 
        widget=forms.TextInput(attrs={'id': 'book_tag_entry'})
        )
    
    def clean_general_tag_list(self):
        data = self.cleaned_data['general_tag_list']
        self._check_for_hash_tags(data)
        return data
    
    def clean_author_tag_list(self):
        data = self.cleaned_data['author_tag_list']
        self._check_for_hash_tags(data)
        return data
    
    def clean_book_tag_list(self):
        data = self.cleaned_data['book_tag_list']
        self._check_for_hash_tags(data)
        return data
    
    def _check_for_hash_tags(self, data):
        for tag in data.split(' '):
            if tag[0] != '#':
                raise ValidationError('# missing in tag')
        return True