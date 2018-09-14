# Generated by Django 2.1.1 on 2018-09-12 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('loader', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('open', models.BooleanField(default=True)),
                ('pltp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loader.PLTP')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('pltp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loader.PLTP')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', jsonfield.fields.JSONField()),
                ('seed', models.CharField(max_length=50, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('grade', models.IntegerField()),
                ('pl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loader.PL')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
