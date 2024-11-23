from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Bookmark
from recipes.models import Recipe

def bookmark_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Bookmark.objects.get_or_create(user=request.user, recipe=recipe)
    return HttpResponseRedirect(reverse('recipes:recipe_detail', args=[recipe_id]))
