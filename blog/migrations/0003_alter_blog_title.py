# Generated by Django 5.1.2 on 2024-10-18 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
