from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest
from  .models import Blog, Category
from django.db.models import Q
from django.shortcuts import redirect, render
from Infohive_main.forms import RegForm
from .models import Blog
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt


# Create your views here.




def home(request):
    try:
        start = int(request.GET.get('start', 3))
        limit = int(request.GET.get('limit', 3))
        if start < 0 or limit <= 0:
            raise ValueError  
    except (TypeError, ValueError):
        start = 3
        limit = 3

    posts = Blog.objects.filter(status="Published").order_by('-created_at')[start:start + limit]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blog/partials/posts.html', {'posts': posts})

    categories = Category.objects.all()
    return render(request, 'blog/home.html', {'posts': posts, 'categories': categories})


def posts_by_category(request, category_id):

    limit = int(request.GET.get('limit', 3))
    start = int(request.GET.get('start', 0))

    posts = Blog.objects.filter(status="Published", category=category_id).order_by('-created_at')[start:start + limit]

    category =  get_object_or_404(Category, pk=category_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blog/partials/posts.html', {'posts': posts})

    context = {
    'posts': posts,
    'category': category,
    }

    return render(request, 'blog/posts_by_categories.html', context)


def register(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('home')
    else:
        form = RegForm()

    context = {
    'form': form, 
    }
    return render(request, 'blog/register.html', context)




def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('home')
        
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'blog/login.html', context)



def logout(request):
    auth.logout(request)
    return redirect('register')




def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blog/blogs.html', {'single_blog': single_blog,})

    context = {
        'single_blog': single_blog,
    }
    return render(request, 'blog/blogs.html', context)


def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains = keyword) | Q(blog_body__icontains = keyword) | Q(short_description__icontains = keyword), status = 'Published')
    context = {
        'blogs': blogs,
        'keyword': keyword,
    }
    return render(request, 'blog/search.html',context)


def dashboards(request):
    return render(request, 'dashboard/dashboards.html')