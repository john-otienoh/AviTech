from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
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

    class Meta:
        """Metadata for models"""
        ordering = ['-publish']
        indexes = [ models.Index(fields=['-publish']), ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Creating cannonical urls"""
        return reverse("aviblog:post_detail", args=[self.slug])
