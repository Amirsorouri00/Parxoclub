# Generated by Django 2.0.7 on 2018-08-13 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0003_expertise'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Expertise',
            new_name='Expertises',
        ),
        migrations.RemoveField(
            model_name='physicians',
            name='Expertise',
        ),
        migrations.AddField(
            model_name='physicians',
            name='expertise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Member.Expertises'),
        ),
    ]