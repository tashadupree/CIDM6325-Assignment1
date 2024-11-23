from django.db import models
from recipes.models import Recipe

class Bookmark(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bookmarked {self.recipe.title}"


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(help_text="List ingredients, one per line.")
    instructions = models.TextField(help_text="Provide detailed cooking instructions.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
