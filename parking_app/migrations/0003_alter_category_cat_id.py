# Generated by Django 4.1.7 on 2023-06-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0002_alter_vehicle_arrival_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
