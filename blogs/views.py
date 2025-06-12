from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from  .models import Blog, Category, PasswordReset
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse


# Create your views here.



@login_required
def home(request):
    try:
        start = int(request.GET.get('start', 3))
        limit = int(request.GET.get('limit', 0))
        if start < 0 or limit <= 0:
            raise ValueError  
    except (TypeError, ValueError):
        start = 3
        limit = 0

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



def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blog/partials/single_blog.html', {'single_blog': single_blog})

    context = {'single_blog': single_blog}
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






def register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")
    
        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")
        
        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            messages.success(request, "Account created. Login now")
            return redirect('login')

    return render(request, 'blog/register.html')




def loginview(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
        
    return render(request, 'blog/login.html')



def logoutview(request):
    auth.logout(request)
    return redirect('login')


def forgotpassword(request):
    if request.method =="POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            email_body = f'Reset your password using the link below:\n\n\n{password_reset_url}',
            email_message =EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.fail_silently = True
            email_message.send()
            return redirect('passwordresetsent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email} found")
            return redirect('forgot_password')
        
    return render(request, 'blog/forgot_password.html')


def passwordresetsent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
      return render(request, 'blog/password_reset_sent.html') 
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot_password')


def resetpassword(request, reset_id):
    try:
        reset_id = PasswordReset,object.get(reset_id=reset_id)
        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False
            if password != confirm_password:
                passwords_have_error =True
                messages.error(request, "Passwords do not match")

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, "Password must be at least 5 characters")
            
            expiration_time = reset_id.created_at + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, "Reset link has expired. Please request a new one.")
                reset_id.delete()

            if not passwords_have_error:
                user = reset_id.user
                user.set_password(password)
                user.save()
                reset_id.delete()
                messages.success(request, "Password reset successfully. You can now login with your new password.")
                return redirect('login')
            
            else:
                return redirect('reset_password', reset_id=reset_id.reset_id)

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot_password')
    
    return render(request, 'blog/reset_password.html')

