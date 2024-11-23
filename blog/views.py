from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.core.mail import send_mail
from .models import Bookmark, Post, Comment, Recipe
from .forms import CommentForm, EmailPostForm
from taggit.models import Tag
from django.contrib.syndication.views import Feed
from .models import Post
from django.db.models import Q
from django.db.models import Count, Avg

def dashboard(request):
    posts_with_comments = Post.published.annotate(total_comments=Count('comments'))
    avg_comments = posts_with_comments.aggregate(avg=Avg('total_comments'))['avg']
    context = {
        'avg_comments': avg_comments,
        # Add other metrics as needed
    }
    return render(request, 'blog/dashboard.html', context)

def post_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.published.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    
    return render(request, 'blog/post/search.html', {'query': query, 'results': results})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']} comments: {cd['comments']}"
            send_mail(subject, message, 'your_email@example.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'blog/recipe_detail.html', {'recipe': recipe})

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED
    )
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts,
        }
    )

def bookmark_list(request):
    bookmarks = Bookmark.objects.all()
    return render(request, 'bookmarks/bookmark_list.html', {'bookmarks': bookmarks})

def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_list_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.published.filter(tags__in=[tag])
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})

def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})


class PostFeed(Feed):
    title = "My Blog Feed"
    link = "/blog/"
    description = "Stay updated with the latest blog posts."

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[:200]  # First 200 characters
