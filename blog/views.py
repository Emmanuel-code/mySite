from django.shortcuts import render,get_object_or_404
from .models import Post
from .models import Comment,Profile
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm,CommentForm,SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm,UserEditForm,ProfileEditForm,BlogAdd
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse

@login_required
def edit(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form=UserEditForm()
        profile_form=ProfileEditForm()
    return render(request, 'blog/profile.html',{'user_form':user_form, 'profile_form':profile_form})


def register(request):
    if request.method=='POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,'registration/register_done.html',{'new_user':new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request,'registration/register.html',{'user_form':user_form})


@login_required
def post_list(request,tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',
                     {'page': page, 'posts': posts,'tag':tag})


@login_required
def add_blog(request):
    if request.method=='POST':
        blog_form=BlogAdd(data=request.POST)
        if blog_form.is_valid():
            new_post=blog_form.save(commit=False)
            new_post.author=request.user
            new_post.publish=timezone.now()
            new_post.save()
            blog_form.save_m2m()
            return redirect('blog:post_detail', pk=new_post.pk)
    else:
        blog_form=BlogAdd()
    return render(request,'blog/add_a_blog.html',{'post_detail':post_detail,'blog_form':blog_form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = BlogAdd(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish = timezone.now()
            post.save()
            post.save_m2m()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = BlogAdd(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post,pk=pk, status='published')
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()

    else:
        comment_form=CommentForm()

    post_tags_ids=post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,'blog/post/detail.html',{'post':	post,
                                                   'comments':comments,
                                                   'new_comment':new_comment,
                                                   'comment_form':comment_form,
                                                   'similar_posts':similar_posts})


@login_required
def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read	"{}"	at	{}\n\n{}\'s	comments:	{}'.format(post.title,	post_url,	cd['name'],	cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent=True

    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html",context={'post':post, 'form':form, 'sent': sent,})


@login_required
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # search_vector = SearchVector('title', weight='A') + SearchVector('body',weight='B')
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.3).order_by('-similarity')
            # search_query = SearchQuery(query)

    return render(request,
                  'blog/post/search.html',
                   {'form': form,
                    'query': query,
                    'results': results})


def profile_view(request):
    profile=Profile.objects.all()
    num_post=Post.published.filter(author=request.user).count()
    context = {
        'profile': profile,
        'num_post':num_post,
    }
    return render(request, "registration/profile.html", context)
