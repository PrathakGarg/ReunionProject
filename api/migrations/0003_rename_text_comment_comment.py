# Generated by Django 4.1.3 on 2022-12-04 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_following_post_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='comment',
        ),
    ]
