# Generated by Django 5.1.2 on 2024-10-27 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='cooking_time',
        ),
        migrations.AddField(
            model_name='recipe',
            name='instructions',
            field=models.TextField(blank=True, default='Instructions not provided'),
        ),
    ]
