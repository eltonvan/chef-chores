# Generated by Django 4.2.6 on 2023-10-31 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='loc_id',
        ),
        migrations.AddField(
            model_name='location',
            name='restaurant_id',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='orders.restaurant'),
            preserve_default=False,
        ),
    ]
