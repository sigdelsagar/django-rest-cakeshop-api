# Generated by Django 3.0.3 on 2020-03-06 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cake', '0002_order_user_ins'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='cakeorder',
            new_name='cakeId',
        ),
    ]
