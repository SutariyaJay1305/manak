# Generated by Django 4.2.7 on 2023-11-30 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_alter_datamanager_d_if_alter_datamanager_d_si1_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datamanager",
            name="D_IF",
            field=models.DecimalField(decimal_places=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name="datamanager",
            name="D_VS1",
            field=models.DecimalField(decimal_places=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name="datamanager",
            name="D_VV1",
            field=models.DecimalField(decimal_places=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name="datamanager",
            name="D_VV2",
            field=models.DecimalField(decimal_places=0, max_digits=5),
        ),
    ]