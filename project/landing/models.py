from django.db import models
from django.utils.text import slugify

class News(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to='news/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-created_at']
