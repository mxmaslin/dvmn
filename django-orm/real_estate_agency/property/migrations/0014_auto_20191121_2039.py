# Generated by Django 2.2.4 on 2019-11-21 17:39

from django.db import migrations


def link_flats_with_owners(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')
    for flat in Flat.objects.all():
        owner, created = Owner.objects.get_or_create(
            name=flat.owner,
            owners_phonenumber=flat.owners_phonenumber,
            owner_phone_pure=flat.owner_phone_pure
        )
        owner.flats.add(flat)


def move_backward(apps, schema_editor):
    Owner = apps.get_model('property', 'Owner')
    for owner in Owner.objects.all():
        owner.flats.clear()


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0013_auto_20191121_0859'),
    ]

    operations = [
        migrations.RunPython(link_flats_with_owners, move_backward)
    ]