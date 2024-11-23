from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),
    path('post/<int:post_id>/share/', views.post_share, name='post_share'),
    path('post/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('feed/', views.PostFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
     path('dashboard/', views.dashboard, name='dashboard'),
]
