from django.urls import include, path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('', views.dashboards, name='dashboards'),
    path(' blogs/<slug:slug>/', views.blogs, name='blogs'),
    path('blogs/search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]