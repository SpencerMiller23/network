# Generated by Django 2.0.3 on 2020-10-25 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_post_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='like',
            new_name='likes',
        ),
    ]
