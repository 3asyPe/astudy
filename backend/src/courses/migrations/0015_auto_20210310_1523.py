# Generated by Django 3.1.7 on 2021-03-10 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_courselecture_courselecturedurationtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courselecture',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
