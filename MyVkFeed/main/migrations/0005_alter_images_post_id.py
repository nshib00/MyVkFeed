# Generated by Django 4.0.5 on 2022-07-26 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
<<<<<<< HEAD

    dependencies = [
        ('main', '0004_alter_images_post_id_alter_post_text'),
=======
    dependencies = [
        ("main", "0004_alter_images_post_id_alter_post_text"),
>>>>>>> dev
    ]

    operations = [
        migrations.AlterField(
<<<<<<< HEAD
            model_name='images',
            name='post_id',
            field=models.ForeignKey(db_constraint=False, default=None, on_delete=django.db.models.deletion.CASCADE, to='main.post', verbose_name='ID поста'),
=======
            model_name="images",
            name="post_id",
            field=models.ForeignKey(
                db_constraint=False,
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.post",
                verbose_name="ID поста",
            ),
>>>>>>> dev
        ),
    ]
