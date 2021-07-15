# Generated by Django 3.2.3 on 2021-07-06 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingprofile',
            name='postal_code',
        ),
        migrations.AlterField(
            model_name='card',
            name='billing_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='billing.billingprofile'),
        ),
    ]