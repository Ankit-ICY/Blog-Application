# blog/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.search import TrigramSimilarity, SearchVector
from django.urls import reverse
from tinymce.models import HTMLField

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # Image field
    title = models.CharField(max_length=255, db_index=True)
    content = HTMLField()
    slug = models.SlugField(max_length=255, unique=True)
    tags = models.ManyToManyField('Tag', related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})  # Adjust 'blog_detail' to your URL name

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)

    def __str__(self):
        return f"{self.user.username} on {self.blog.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    