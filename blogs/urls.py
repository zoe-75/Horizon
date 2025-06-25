from django.urls import include, path
from .import views



urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('', views.dashboards, name='dashboards'),
    path('blogs/<slug:slug>/', views.blogs, name='blogs'),
    path('blogs/search/', views.search, name='search'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('forgot_password/', views.ForgotPassword, name='forgot_password'),
    path('reset_password/<str:reset_id>/', views. ResetPassword, name='reset_password'),
    path('logout/', views.LogoutView, name='logout'),
    path('password_reset_sent/<str:reset_id>/', views.PasswordResetSent, name='password_reset_sent'),
    path('complete-social-signup/', views.complete_social_signup, name='complete_social_signup'),
]