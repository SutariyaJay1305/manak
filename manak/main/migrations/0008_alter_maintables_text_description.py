# Generated by Django 4.2.7 on 2024-01-31 07:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_alter_datamanager_d_if_alter_datamanager_d_si1_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="maintables",
            name="text_description",
            field=models.TextField(max_length=500),
        ),
    ]