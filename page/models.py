# coding: utf-8
from django.db import models


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

    def __str__(self):
        s = self.name
        if not self.in_stock:
            s = '{} (нет в наличии)'.format(s)
        return s


class BlogArticle(models.Model):
    title = models.CharField(max_length=256, unique_for_month='pubdate')
    pubdate = models.DateField()
    updated = models.DateTimeField(auto_now=True)
