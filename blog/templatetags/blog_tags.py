from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

# Initialize the template library
register = template.Library()

# Markdown filter
@register.filter(name='markdown')
def markdown_format(text):
    """Converts text to HTML using markdown."""
    return mark_safe(markdown.markdown(text))

# Simple tag to count total published posts
@register.simple_tag
def total_posts():
    """Returns the total count of published posts."""
    return Post.published.count()

# Inclusion tag to show latest posts
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """Returns the latest published posts."""
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# Simple tag to get the most commented posts
@register.simple_tag
def get_most_commented_posts(count=5):
    """Returns the most commented published posts."""
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]
