# Generated by Django 4.2.4 on 2023-08-12 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_news_has_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='has_comments',
            field=models.BooleanField(),
        ),
    ]
