# Generated by Django 2.1.1 on 2018-09-29 10:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group_For_Objects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GroupDoesntHavePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupHavePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectId', models.DecimalField(decimal_places=3, max_digits=3)),
                ('className', models.CharField(max_length=40)),
                ('idName', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ObjectGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Common.Group_For_Objects')),
                ('pageObject_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Common.Object')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pageId', models.DecimalField(decimal_places=3, max_digits=3)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together={('id', 'name')},
        ),
        migrations.AddField(
            model_name='object',
            name='page_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Common.Page'),
        ),
    ]
