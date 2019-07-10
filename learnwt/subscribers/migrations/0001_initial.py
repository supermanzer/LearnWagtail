# Generated by Django 2.2.3 on 2019-07-10 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(help_text='Enter email address', max_length=100)),
                ('first_name', models.CharField(help_text='Enter first name', max_length=100)),
                ('last_name', models.CharField(help_text='Enter last name', max_length=100)),
            ],
        ),
    ]
