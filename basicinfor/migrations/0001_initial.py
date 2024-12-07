# Generated by Django 5.1.3 on 2024-12-07 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
    ]
