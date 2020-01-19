
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class PublishedManager(models.Manager):
    def	get_queryset(self):
        return super(PublishedManager,	self).get_queryset()\
            .filter(status='published')


class Post(models.Model):
    objects = models.Manager()  # The	default	manager.
    published = PublishedManager()
    tags=TaggableManager()

    STATUS_CHOICES = (('draft',	'Draft'),('published',	'Published'),)
    title=models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated	= models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='published')

    def get_absolute_url(self):
        return reverse('blog:post_detail',	args=[str(self.pk)])

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name=models.CharField(max_length=80)
    # email=models.EmailField()
    body=models.CharField(max_length=160)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)