# Generated by Django 4.1.7 on 2023-03-28 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbsnote', '0003_comment_author_comment_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]