# Generated by Django 4.2.3 on 2024-01-27 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_my_field_coaches_coed_allgirl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coaches',
            name='coed_allgirl',
            field=models.CharField(choices=[('Coed', 'Coed'), ('All-Girl', 'All-Girl')], default='Coed', max_length=10),
        ),
    ]
