# Generated by Django 5.0.6 on 2024-05-24 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_payment_card_number_alter_payment_cvv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='city',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
