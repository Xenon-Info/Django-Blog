from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name="posts"),

    path('', views.posts, name="posts"),

    path('post/<str:pk>/', views.post, name="post"),

    path('create-post/', views.create_post, name="create-post"),

    path('update-post/<str:pk>/', views.update_post, name="update-post"),

    path('delete-post/<str:pk>/', views.delete_post, name="delete-post"),
]
