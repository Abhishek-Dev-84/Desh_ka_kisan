# Generated by Django 5.2.1 on 2025-06-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0014_order_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='username',
            field=models.CharField(default='unknown', max_length=100),
        ),
    ]
