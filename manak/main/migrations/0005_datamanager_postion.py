# Generated by Django 4.2.7 on 2023-11-21 04:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_alter_datamanager_current_percentage_change_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="datamanager",
            name="postion",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
