# Generated by Django 5.0.1 on 2024-04-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdrama', '0011_remove_movie_runtime_movie_episodes_movie_seasons'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='episode_length',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]