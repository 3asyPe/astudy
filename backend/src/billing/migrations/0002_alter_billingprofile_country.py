# Generated by Django 3.2 on 2021-05-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingprofile',
            name='country',
            field=models.CharField(default='United States of America', max_length=120),
        ),
    ]
