from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        """Return  queryset of objects to include in the sitemap"""
        return Post.objects.filter(status=Post.Status.PUBLISHED)
    
    def lastmod(self, obj):
        """Return last time object was modified"""
        return obj.updated
    