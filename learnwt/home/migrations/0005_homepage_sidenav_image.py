# Generated by Django 2.2.3 on 2019-07-04 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('home', '0004_auto_20190704_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='sidenav_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
