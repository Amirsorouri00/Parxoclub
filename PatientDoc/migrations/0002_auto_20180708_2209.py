# Generated by Django 2.0.7 on 2018-07-08 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PatientDoc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doccategories',
            name='icon',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
