# Generated by Django 4.2.3 on 2024-02-01 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_coaches_coach_tumbling'),
    ]

    operations = [
        migrations.AddField(
            model_name='coaches',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
