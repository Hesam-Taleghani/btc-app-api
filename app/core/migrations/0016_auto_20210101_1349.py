# Generated by Django 3.1.4 on 2021-01-01 13:49

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20201226_1550'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bonus',
            new_name='MIDRevenue',
        ),
        migrations.AddField(
            model_name='contract',
            name='e_commerce_m_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name='costumer',
            name='note',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='pos',
            name='note',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='amex_m_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='annual_card_turnover',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='contract',
            name='annual_total_turnover',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='contract',
            name='atv',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='contract',
            name='authorizathion_fee',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='contract',
            name='face_to_face_saled',
            field=models.PositiveIntegerField(validators=[core.models.percent_validator]),
        ),
        migrations.AlterField(
            model_name='contract',
            name='interchange',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='contract',
            name='m_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='pci_dss',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='contract',
            name='t_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='business_email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='business_postal_code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='company_number',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='director_address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='director_email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='director_name',
            field=models.CharField(max_length=110),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='director_phone',
            field=models.CharField(max_length=55),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='director_postal_code',
            field=models.CharField(max_length=55),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='land_line',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='registered_postal_code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='marketinggoal',
            name='note',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
