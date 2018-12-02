# Generated by Django 2.1.3 on 2018-12-02 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_auto_20181125_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='thumbnail',
            field=models.ImageField(blank=True, height_field='thumbnail_height', null=True, upload_to='goods/thumbnails', width_field='thumbnail_width'),
        ),
        migrations.AddField(
            model_name='good',
            name='thumbnail_height',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='good',
            name='thumbnail_width',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]