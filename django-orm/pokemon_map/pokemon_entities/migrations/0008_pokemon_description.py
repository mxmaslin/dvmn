# Generated by Django 2.2.3 on 2019-11-15 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0007_auto_20191114_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
