# Generated by Django 4.1.1 on 2023-10-02 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_product_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Out for delivery", "Out for delivery"),
                    ("Delivered", "Delivery"),
                ],
                max_length=200,
                null=True,
            ),
        ),
    ]
