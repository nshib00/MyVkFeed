# Generated by Django 4.0.5 on 2022-08-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_images_post_id_images_post_post_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='group',
        ),
        migrations.AddField(
            model_name='post',
            name='by_hidden_group',
            field=models.BooleanField(default=0, verbose_name='Пост скрытой группы'),
        ),
    ]