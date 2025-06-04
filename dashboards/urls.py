from django.urls import path
from .import views

urlpatterns = [
    path('dashboards/', views.dashboard, name='dashboards'),
    path('categories', views.categories, name='categories'),
    path('categories/add', views.add_categories, name='add_categories'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    path('dashboards/add', views.add_posts, name='add_posts'),
    path('dashboards/edit/<int:pk>/', views.edit_posts, name='edit_posts'),
    path('dashboards/delete/<int:pk>/', views.delete_posts, name='delete_posts'),
]