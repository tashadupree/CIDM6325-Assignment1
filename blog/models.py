from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from django.shortcuts import render


def dashboard(request):
    total_posts = Post.published.count()
    total_comments = Comment.objects.count()
    total_recipes = Recipe.objects.count()
    latest_comments = Comment.objects.order_by('-created')[:5]

    context = {
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_recipes': total_recipes,
        'latest_comments': latest_comments,
    }

    return render(request, 'blog/dashboard.html', context)



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    tags = TaggableManager()

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    content = models.TextField(default="Default content for existing posts")
    image = models.ImageField(upload_to='blog_posts/', blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager()  
    published = PublishedManager()  

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

    def __str__(self):
        return self.title


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Appetizer', 'Appetizer'),
        ('Main Course', 'Main Course'),
        ('Dessert', 'Dessert'),
        ('Beverage', 'Beverage'),
    ]
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    body = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField(blank=True, default="Instructions not provided")
    servings = models.PositiveIntegerField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cuisine = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def get_absolute_url(self):
        return reverse(
            'blog:recipe_detail',  
            args=[self.id]
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='bookmarked_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bookmarked {self.post}"
    


