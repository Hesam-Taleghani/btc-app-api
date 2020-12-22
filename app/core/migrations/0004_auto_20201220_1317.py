# Generated by Django 3.1.4 on 2020-12-20 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='postal_code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]