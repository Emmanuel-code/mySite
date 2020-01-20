from django.urls import path
from . import views

app_name = 'person'
urlpatterns = [
    path('profile/',views.profile_view, name='profile'),
    path('about/',views.about_view, name='about'),
]
