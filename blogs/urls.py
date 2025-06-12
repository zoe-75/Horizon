from django.urls import include, path
from .import views



urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('', views.dashboards, name='dashboards'),
    path('blogs/<slug:slug>/', views.blogs, name='blogs'),
    path('blogs/search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('forgot_password/', views.forgotpassword, name='forgot_password'),
    path('reset_password/<str:reset_id>/', views.resetpassword, name='reset_password'),
    path('logout/', views.logoutview, name='logout'),
    path('password_reset_sent/<str:reset_id>/', views.passwordresetsent, name='password_reset_sent'),
]