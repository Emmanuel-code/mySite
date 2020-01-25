from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'
urlpatterns = [

    path('', views.post_list,name='post_list'),
    path('<int:pk>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/',LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('register/', views.register, name='register'),


]
