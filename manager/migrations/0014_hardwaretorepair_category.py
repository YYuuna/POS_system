# Generated by Django 4.2.10 on 2024-05-02 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0013_hardwaretorepair_remove_product_initial_buying_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardwaretorepair',
            name='category',
            field=models.ForeignKey(db_column='Catégorie', default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='manager.category'),
        ),
    ]
