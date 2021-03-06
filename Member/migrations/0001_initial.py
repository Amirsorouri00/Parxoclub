# Generated by Django 2.1.1 on 2018-09-29 10:57

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expertises',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('rtl_name', models.CharField(blank=True, default='قلب', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group_Give_Perm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('index', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Group_Have_Perm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('index', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('code', models.CharField(blank=True, db_index=True, max_length=20, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='member_user', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Memberships',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rtl_name', models.CharField(blank=True, default='طلایی', max_length=50, null=True)),
                ('index', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Physicians',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='physician_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('expertise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='physician_expertise', to='Member.Expertises')),
            ],
        ),
        migrations.CreateModel(
            name='Prefixes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('rtl_name', models.CharField(blank=True, default='دکتر', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='profile_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('code', models.CharField(db_index=True, max_length=20, unique=True)),
                ('rtl_first_name', models.CharField(blank=True, default='تست', max_length=50, null=True)),
                ('rtl_last_name', models.CharField(blank=True, default='تست', max_length=50, null=True)),
                ('pkey', models.CharField(blank=True, max_length=100, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('maleOrFemale', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=8)),
                ('gender', models.BooleanField(default=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('photo', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('haveOrGive', models.CharField(choices=[('have', 'have'), ('give', 'give')], max_length=5)),
                ('groupG', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Member.Group_Give_Perm')),
                ('groupH', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Member.Group_Have_Perm')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='physicians',
            name='prefix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='physician_prefix', to='Member.Prefixes'),
        ),
        migrations.AddField(
            model_name='members',
            name='membership',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='member_membership', to='Member.Memberships'),
        ),
        migrations.AddField(
            model_name='members',
            name='physician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='member_physician', to='Member.Physicians'),
        ),
        migrations.AddField(
            model_name='members',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='member_profile', to='Member.Profile'),
        ),
        migrations.AddField(
            model_name='group_have_perm',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group_give_perm',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usergroup',
            unique_together={('user_id', 'haveOrGive')},
        ),
    ]
