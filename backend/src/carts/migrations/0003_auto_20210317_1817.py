# Generated by Django 3.1.7 on 2021-03-17 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_auto_20210314_1433'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Cart', 'verbose_name_plural': 'Carts'},
        ),
    ]