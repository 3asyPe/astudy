# Generated by Django 3.1.7 on 2021-03-09 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20210309_1425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursecontent',
            old_name='section_count',
            new_name='sections_count',
        ),
    ]
