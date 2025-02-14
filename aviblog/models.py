from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from taggit.managers import TaggableManager
from django.conf import settings
# Create your models here.

class Post(models.Model):
    """Post model that will allow us to store blog posts in the database."""
    class Status(models.TextChoices):
        """status of blog posts"""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        ARCHIVED = 'AR', 'Archived'

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique_for_date='publish')
    publish = models.DateTimeField(timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT, verbose_name='Status')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts' )
    body = models.TextField()
    tags = TaggableManager()

    class Meta:
        """Metadata for the Post model"""
        ordering = ['-publish']
        indexes = [ models.Index(fields=['-publish']), ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Creating cannonical urls"""
        return reverse("aviblog:post_detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        # Automatically generate slug from title
        if not self.slug:  # Only set slug if it is not already set
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    """Comment System"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=25)
    body = models.TextField()
    commented = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        """Metadata for the Comment Model"""
        ordering = ['commented']
        indexes = [models.Index(fields=['commented'])]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    