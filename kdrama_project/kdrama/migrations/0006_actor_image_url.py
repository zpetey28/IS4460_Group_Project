# Generated by Django 5.0.2 on 2024-04-12 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdrama', '0005_movie_awards'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='image_url',
            field=models.URLField(blank=True, default='https://i.pinimg.com/736x/c0/74/9b/c0749b7cc401421662ae901ec8f9f660.jpg'),
        ),
    ]
