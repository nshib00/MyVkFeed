# Generated by Django 4.0.5 on 2022-08-18 07:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0010_remove_post_group_post_by_hidden_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="images",
            name="image",
            field=models.ImageField(
                blank=True,
                db_index=True,
                null=True,
                upload_to="photos/%Y/%m/%d",
                verbose_name="Фото",
            ),
        ),
    ]
