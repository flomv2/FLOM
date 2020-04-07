# Generated by Django 2.2 on 2020-02-21 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('roomID', models.CharField(max_length=5)),
                ('totalOccupants', models.IntegerField(default=0)),
                ('avgOccLength', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('roomID', models.CharField(max_length=5)),
                ('totalOccupants', models.IntegerField(default=0)),
                ('avgOccLength', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='StatsLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.IntegerField(default=0)),
                ('roomID', models.CharField(max_length=5)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('roomID', models.CharField(max_length=5)),
                ('totalOccupants', models.IntegerField(default=0)),
                ('avgOccLength', models.DurationField()),
            ],
        ),
    ]