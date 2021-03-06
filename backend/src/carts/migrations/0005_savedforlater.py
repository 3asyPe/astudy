# Generated by Django 3.1.7 on 2021-03-29 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0022_auto_20210317_1857'),
        ('carts', '0004_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedForLater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('courses', models.ManyToManyField(blank=True, to='courses.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Saved for later list',
                'verbose_name_plural': 'Saved for later lists',
            },
        ),
    ]
