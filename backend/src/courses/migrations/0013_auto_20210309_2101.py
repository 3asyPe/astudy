# Generated by Django 3.1.7 on 2021-03-09 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20210309_2059'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SectionDurationTime',
            new_name='CourseSectionDurationTime',
        ),
    ]
