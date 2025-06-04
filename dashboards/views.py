from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from dashboards.forms import CategoryForm, BlogPostForm
from django.template.defaultfilters import slugify
# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count() 
    blogs_count = Blog.objects.all().count()
    posts = Blog.objects.all()
    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
        'posts': posts,
    }
    return render(request, 'dashboard/dashboards.html', context)

def posts(request):
    return render(request, 'dashboard/dashboards.html')


def categories(request):
    return render(request, 'dashboard/dashboards.html')



def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboards')
    form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_categories.html', context)


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboards')

    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboard/edit_category.html', context)


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('dashboards')




def add_posts(request):
    if request.method == 'POST':
        form = BlogPostForm( request.POST, request.FILES)
        if form.is_valid():
            post =  form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('dashboards')
        
    form =  BlogPostForm()
    context ={
        'form': form,
    }
    return render(request, 'dashboard/add_posts.html', context)


def edit_posts(request, pk):
    posts = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm( request.POST, request.FILES, instance=posts)
        if form.is_valid():
            post =  form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('dashboards')
        
    form = BlogPostForm(instance=posts)
    context = {
        'form': form,
        'posts': posts
    }
    return render(request, 'dashboard/edit_posts.html', context)


def delete_posts(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('dashboards')
