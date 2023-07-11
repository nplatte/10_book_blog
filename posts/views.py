from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from posts.forms import PostModelForm, TagForm
from posts.models import Post, Tag
from django.core.exceptions import ObjectDoesNotExist

def home_page(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'general_tags': Tag.objects.filter(group_name='general'),
        'author_tags': Tag.objects.filter(group_name='author'),
        'book_tags': Tag.objects.filter(group_name='book'),
        }
    return render(request, 'posts/home.html', context)

@login_required
def create_post_page(request):
    new_post_form = PostModelForm()
    post_tags_form = TagForm()
    context = {
        'new_post_form': new_post_form, 
        'post_tags_form': post_tags_form}
    if request.method == "POST":
        new_post_form =  PostModelForm(request.POST)
        post_tags = TagForm(request.POST)
        if new_post_form.is_valid() and post_tags.is_valid():
            new_post = new_post_form.save()
            _add_tags(new_post, request.POST['tag_list'])
            return redirect(reverse('home_page'))

    return render(request, 'posts/create.html', context)

def _add_tags(post, tag_list):
    tags = tag_list.split(' ')
    for tag in tags:
        try:
            tag_to_add = Tag.objects.get(tag_name=tag)
        except ObjectDoesNotExist:
            tag_to_add = Tag.objects.create(tag_name=tag)
        post.tags.add(tag_to_add)

def view_post_page(request):
    return render(request, 'posts/view.html')
