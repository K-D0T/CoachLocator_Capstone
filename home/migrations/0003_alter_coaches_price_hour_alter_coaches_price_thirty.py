# Generated by Django 4.2.3 on 2024-02-07 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_coaches_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coaches',
            name='price_hour',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coaches',
            name='price_thirty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
