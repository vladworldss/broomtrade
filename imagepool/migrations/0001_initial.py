# Generated by Django 2.1.3 on 2018-12-22 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagePool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Выгружен')),
                ('image', models.ImageField(upload_to='imagepool/%Y/%m', verbose_name='Изображение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
                'ordering': ['user', '-uploaded'],
            },
        ),
    ]
