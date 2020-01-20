from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'
urlpatterns = [

    path('', views.post_list,name='post_list'),
    path('add/', views.add_blog, name='add_blog'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/',LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('register/', views.register, name='register'),

    path('edit_profile/', views.edit, name='edit'),

]
