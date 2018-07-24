# Generated by Django 2.0.7 on 2018-07-11 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Member', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('index', models.IntegerField(default=0)),
                ('icon', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('attachment', models.PositiveIntegerField(default=0)),
                ('comment', models.CharField(blank=True, max_length=1000, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PatientDoc.DocCategories')),
                ('physician', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Member.Physicians')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]