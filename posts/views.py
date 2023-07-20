from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from posts.forms import PostModelForm, TagForm
from posts.models import Post, Tag
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.core import serializers



def home_page(request):
    posts = Post.objects.all()
    tag_groups = [
        Tag.objects.filter(group_name='general'),
        Tag.objects.filter(group_name='author'),
        Tag.objects.filter(group_name='book'),
    ]
    context = {
        'posts': posts,
        'tag_groups': tag_groups
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
            _add_tags(new_post, request.POST['general_tag_list'], 'general')
            _add_tags(new_post, request.POST['author_tag_list'], 'author')
            _add_tags(new_post, request.POST['book_tag_list'], 'book')
            return redirect(reverse('home_page'))

    return render(request, 'posts/create.html', context)

def _add_tags(post, tag_list, tag_type):
    tags = tag_list.split(' ')
    for tag in tags:
        try:
            tag_to_add = Tag.objects.get(tag_name=tag)
        except ObjectDoesNotExist:
            tag_to_add = Tag.objects.create(tag_name=tag, group_name=tag_type)
        post.tags.add(tag_to_add)

def view_post_page(request):
    return render(request, 'posts/view.html')

def ajax_call(request):
    tag_dict = request.POST.dict()
    tag = _toggle_tag(tag_dict['tag'])
    posts = _get_posts()
    data = serializers.serialize('json', posts)
    return HttpResponse(data)

def _get_posts():
    active_tagged = Post.objects.filter(tags__status='active')
    excluded_tagged = Post.objects.exclude(tags__status='inactive')
    if len(active_tagged) > 0 and len(excluded_tagged) > 0:
        return Post.objects.filter(tags__status='active').exclude(tags__status='inactive')
    elif len(active_tagged) > 0:
        return active_tagged
    elif len(excluded_tagged) > 0:
        return excluded_tagged
    return Post.objects.all()

def _toggle_tag(tag_name):
    tag_to_toggle = Tag.objects.get(tag_name=tag_name)
    if tag_to_toggle.status == 'active':
        tag_to_toggle.status = 'inactive'
    elif tag_to_toggle.status == 'inactive':
        tag_to_toggle.status = 'none'
    elif tag_to_toggle.status == 'none':
        tag_to_toggle.status = 'active'
    tag_to_toggle.save()
    return tag_to_toggle