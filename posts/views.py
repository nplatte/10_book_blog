from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from posts.forms import PostModelForm
from posts.models import Post

def home_page(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts})

@login_required
def create_post_page(request):
    new_post_form = PostModelForm()
    if request.method == "POST":
        new_post_form =  PostModelForm(request.POST)
        if new_post_form.is_valid():
            new_post_form.save()
            return redirect(reverse('view_post'))

    return render(request, 'posts/create.html', {'new_post_form': new_post_form})

def view_post_page(request):
    return render(request, 'posts/view.html')
