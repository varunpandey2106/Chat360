# Generated by Django 4.2.3 on 2023-08-13 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Text360', '0002_alter_room_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='messages',
            field=models.ManyToManyField(blank=True, to='Text360.message'),
        ),
    ]