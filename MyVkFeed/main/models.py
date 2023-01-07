from django.db import models
from django.urls import reverse


class Post(models.Model):
    date = models.CharField(max_length=16, verbose_name='Дата публикации')
    title = models.CharField(null=True, blank=True, max_length=255, verbose_name='Автор поста')
    text = models.TextField(default=None, null=True, verbose_name='Текст')
    accurate_date = models.IntegerField(default=0, db_index=True)
    photo_count = models.IntegerField(default=0, verbose_name='Количество фото')
    by_hidden_group = models.BooleanField(default=0, verbose_name='Пост скрытой группы')
    photos = models.ManyToManyField('Images', blank=True, related_name='post_photos')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-accurate_date']

    def __str__(self): return f'Post #{self.pk}'

    def get_absolute_url(self): return reverse('post', kwargs={'pk': self.pk})

    def get_post_id(self): return self.pk


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='ID поста', null=True)
    image = models.ImageField(null=True, blank=True, upload_to='photos/%Y/%m/%d', verbose_name='Фото', db_index=True)

    class Meta:
        ordering = ['post_id']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'Image #{self.pk}'


class Group(models.Model):
    group_title = models.CharField(max_length=100, verbose_name='Название')
    is_hidden = models.BooleanField(default=False, verbose_name='Скрытая группа')
    image = models.ImageField(upload_to='photos/groups/%Y/%m/%d', verbose_name='Аватар группы', null=True, default=None)

    class Meta:
        ordering = ['group_title']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.group_title

    def get_absolute_url(self):
        return reverse('group', kwargs={'pk': self.pk})
