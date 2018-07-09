# Generated by Django 2.0.6 on 2018-07-05 11:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playexo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('label', models.CharField(max_length=20)),
                ('activity', models.ManyToManyField(blank=True, to='playexo.Activity')),
                ('student', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ManyToManyField(blank=True, related_name='teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
