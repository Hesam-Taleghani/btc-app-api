# Generated by Django 3.1.4 on 2020-12-24 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20201224_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pos',
            name='type',
            field=models.CharField(choices=[('D', 'Desktop'), ('M', 'Mobile'), ('P', 'Portable')], max_length=25),
        ),
    ]
