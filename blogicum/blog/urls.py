from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]
