# Generated by Django 4.0.5 on 2022-08-31 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_group_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='images',
            options={'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-accurate_date'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.RemoveField(
            model_name='images',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ManyToManyField(blank=True, to='main.images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='accurate_date',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
