# Generated by Django 5.1.3 on 2024-11-13 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_alter_booking_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='hotel_description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_description_ky',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_description_tr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_name_en',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_name_ky',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_name_ru',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_name_tr',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
