# Generated by Django 5.0.7 on 2024-08-10 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_book_owner_userbookrelation_book_readers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbookrelation',
            old_name='read',
            new_name='in_bookmarks',
        ),
    ]
