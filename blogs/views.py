from django import forms
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
#HOME
@login_required
def home(request):
    try:
        start = int(request.GET.get('start', 0))
        limit = int(request.GET.get('limit', 0))
        if start < 0 or limit <= 0:
            raise ValueError  
    except (TypeError, ValueError):
        start = 0
        limit = 0
    posts = Blog.objects.filter(status="Published").order_by('-created_at')[start:start + limit]
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blog/partials/posts.html', {'posts': posts})
    categories = Category.objects.all()
    return render(request, 'blog/home.html', {'posts': posts, 'categories': categories})


#POSTS_BY_CATEGORY
def posts_by_category(request, category_id):
    start = int(request.GET.get('start', 0))
    limit = int(request.GET.get('limit', 3))  # default to 3
    posts = Blog.objects.filter(status="Published", category=category_id).order_by('-created_at')[start:start + limit]
    category =  get_object_or_404(Category, pk=category_id)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blog/partials/posts.html', {'posts': posts})
    context = {
    'posts': posts,
    'category': category,
    }
    return render(request, 'blog/posts_by_categories.html', context)

#BLOG_POST
def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blog/partials/single_blog.html', {'single_blog': single_blog})
    context = {'single_blog': single_blog}
    return render(request, 'blog/blogs.html', context)

#SEARCH_CODE

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains = keyword) | Q(blog_body__icontains = keyword) | Q(short_description__icontains = keyword), status = 'Published')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'blog/partials/posts.html', {'blogs ': blogs})

    return render(request, 'blog/search.html', {'blogs ': blogs , 'keyword': keyword})



#DASHBOARDS
def dashboards(request):
    return render(request, 'dashboard/dashboards.html')


#AUTHENTICATION____________________________
#REGISTER
def RegisterView(request):

    if request.method == "POST":
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
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
                # first_name=first_name,
                # last_name=last_name,
                email=email, 
                username=username,
                password=password
            )
            messages.success(request, "Account created. Login now")
            return redirect('login')

    return render(request, 'blog/register.html')



class UsernameOnlyForm(forms.Form):
    username = forms.CharField(max_length=30)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


from allauth.socialaccount.models import SocialLogin, SocialAccount
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from .forms import UsernameOnlyForm

def complete_social_signup(request):
    sociallogin = request.session.get('socialaccount_sociallogin')

    if not sociallogin:
        return redirect('account_login')

    form = UsernameOnlyForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data['username']
        sociallogin = SocialLogin.deserialize(sociallogin)
        user = sociallogin.user
        user.username = username
        user.save()
        return complete_signup(request, sociallogin, allauth_settings.EMAIL_VERIFICATION, '/')
    
    return render(request, 'socialaccount/username_signup.html', {'form': form})



def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'blog/login.html')

def LogoutView(request):

    logout(request)

    return redirect('login')

def ForgotPassword(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset_password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = False
            email_message.send()

            return redirect('password_reset_sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot_password')

    return render(request, 'blog/forgot_password.html')

def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'blog/password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot_password')

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters')

            expiration_time = password_reset_id.created_at + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset successful. You can now log in with your new password.')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset_password', reset_id=reset_id)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot_password')

    return render(request, 'blog/reset_password.html')