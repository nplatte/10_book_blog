from django.shortcuts import render

def home_page(request):
    return render(request, 'posts/home.html')

def create_post_page(request):
    return render(request, 'posts/create.html')

def view_post_page(request):
    return render(request, 'posts/view.html')
