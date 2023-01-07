# Generated by Django 4.0.5 on 2022-07-25 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_post_photo_ref_alter_images_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='post_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.post', verbose_name='ID поста'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, default=None, verbose_name='Текст'),
        ),
    ]
