from django.shortcuts import render
from .models import Profile1,About
from blog.models import Post


def about_view(request):
    about=About.objects.all()
    return render(request,'person/about.html',{'about':about})


def profile_view(request):
    profile=Profile1.objects.all()
    num_post=Post.published.filter(author=request.user).count()
    context = {
        'profile': profile,
        'num_post':num_post,
    }
    return render(request, "person/profile.html", context)

