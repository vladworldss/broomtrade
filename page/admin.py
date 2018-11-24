from django.contrib import admin
from page.models import Category, Good

admin.register(Category, Good)(admin.ModelAdmin)
