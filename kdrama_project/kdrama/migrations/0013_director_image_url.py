# Generated by Django 5.0.1 on 2024-04-14 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdrama', '0012_movie_episode_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='image_url',
            field=models.URLField(blank=True, max_length=9223372036854775807),
        ),
    ]
