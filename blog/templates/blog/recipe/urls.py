from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),  # List all recipes
    path('<int:id>/', views.recipe_detail, name='recipe_detail'),  # View a single recipe
]
