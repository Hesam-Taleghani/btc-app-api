# Generated by Django 3.1.4 on 2020-12-24 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_pos_poscompany_posmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pos',
            old_name='pos_type',
            new_name='type',
        ),
    ]