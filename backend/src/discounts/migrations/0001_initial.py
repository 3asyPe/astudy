# Generated by Django 3.1.7 on 2021-04-04 12:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0022_auto_20210317_1857'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0006_auto_20210330_2106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('discount', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('expires', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('applicable_to', models.ManyToManyField(related_name='coupons', to='courses.Course')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.CreateModel(
            name='AppliedCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('applied_to', models.ManyToManyField(to='courses.Course')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.coupon')),
            ],
        ),
    ]