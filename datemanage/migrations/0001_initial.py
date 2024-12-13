# Generated by Django 5.1.3 on 2024-12-13 02:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendancetable',
            fields=[
                ('recordid', models.AutoField(db_column='RecordID', primary_key=True, serialize=False)),
                ('clockintime', models.TimeField(blank=True, db_column='ClockInTime', null=True)),
                ('clockouttime', models.TimeField(blank=True, db_column='ClockOutTime', null=True)),
            ],
            options={
                'db_table': 'attendancetable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Employeetable',
            fields=[
                ('employeeid', models.AutoField(db_column='EmployeeID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=100)),
                ('gender', models.CharField(db_column='Gender', max_length=6)),
                ('phonenumber', models.CharField(blank=True, db_column='PhoneNumber', max_length=20, null=True)),
            ],
            options={
                'db_table': 'employeetable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Performanceevaluationtable',
            fields=[
                ('employeeid', models.IntegerField(db_column='EmployeeID', primary_key=True, serialize=False)),
                ('score', models.DecimalField(db_column='Score', decimal_places=2, max_digits=5)),
                ('evaluationdate', models.DateField(db_column='EvaluationDate')),
            ],
            options={
                'db_table': 'performanceevaluationtable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Performancetable',
            fields=[
                ('indicatorname', models.CharField(db_column='IndicatorName', max_length=100, primary_key=True, serialize=False)),
                ('weight', models.DecimalField(db_column='Weight', decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'performancetable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Workdaytable',
            fields=[
                ('date', models.DateField(db_column='Date', primary_key=True, serialize=False)),
                ('isworkday', models.IntegerField(db_column='IsWorkday')),
            ],
            options={
                'db_table': 'workdaytable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bonustable',
            fields=[
                ('BonusID', models.AutoField(db_column='BonusID', primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paymentdate', models.DateField()),
                ('reason', models.TextField()),
            ],
            options={
                'db_table': 'bonustable',
            },
        ),
        migrations.CreateModel(
            name='Employeebonustable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paymentdate', models.DateField()),
                ('reason', models.TextField()),
                ('bonus', models.ForeignKey(db_column='BonusID', on_delete=django.db.models.deletion.CASCADE, to='datemanage.bonustable')),
                ('employee', models.ForeignKey(db_column='EmployeeID', on_delete=django.db.models.deletion.CASCADE, to='datemanage.employeetable')),
            ],
            options={
                'db_table': 'employeebonustable',
            },
        ),
    ]
