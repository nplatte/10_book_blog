from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home_page(request):
    return render(request, 'posts/home.html')

@login_required
def create_post_page(request):
    if request.method == "POST":
        pass
    return render(request, 'posts/create.html')

def view_post_page(request):
    return render(request, 'posts/view.html')
