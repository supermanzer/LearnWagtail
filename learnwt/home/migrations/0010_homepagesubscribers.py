# Generated by Django 2.2.3 on 2019-07-10 13:49

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0002_auto_20190710_1349'),
        ('home', '0009_homepagecarousel_text_orient'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageSubscribers',
            fields=[
                ('subscriber_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subscribers.Subscriber')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='homepage_subscribers', to='home.HomePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('subscribers.subscriber', models.Model),
        ),
    ]
