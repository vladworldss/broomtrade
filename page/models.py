# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Good(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    in_stock = models.BooleanField(default=True, db_index=True, verbose_name='В наличии')
    thumbnail_width = models.PositiveSmallIntegerField(null=True, blank=True)
    thumbnail_height = models.PositiveSmallIntegerField(null=True, blank=True)
    thumbnail = models.ImageField(null=True,
                                  blank=True,
                                  upload_to='goods/thumbnails',
                                  width_field='thumbnail_width',
                                  height_field='thumbnail_height',
                                  )

    class Meta:
        ordering = ('-price', 'name')
        unique_together = ('category', 'name', 'price')
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def get_is_stock(self):
        if self.in_stock:
            return '+'
        else:
            return ''

    def save(self, *args, **kw):
        try:
            this_record = Good.objects.get(id=self.id)
            if this_record.thumbnail != self.thumbnail:
                this_record.thumbnail.delete(save=False)
        except Good.DoesNotExist:
            pass
        return super().save(*args, **kw)

    def delete(self, *args, **kw):
        self.thumbnail.delete(save=False)
        return super().delete(*args, **kw)

    def __str__(self):
        s = self.name
        if not self.in_stock:
            s = '{} (нет в наличии)'.format(s)
        return s


class BlogArticle(models.Model):
    title = models.CharField(max_length=256, unique_for_month='pubdate')
    pubdate = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
