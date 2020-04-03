# Generated by Django 2.2.4 on 2019-11-21 05:41

from django.conf import settings
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0010_auto_20191121_0800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ФИО владельца')),
                ('owners_phonenumber', models.CharField(max_length=20, verbose_name='Номер владельца')),
                ('owner_phone_pure', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, verbose_name='Нормализованный номер телефона')),
                ('flats', models.ManyToManyField(blank=True, related_name='owners', to=settings.AUTH_USER_MODEL, verbose_name='Квартиры в собственности')),
            ],
        ),
    ]