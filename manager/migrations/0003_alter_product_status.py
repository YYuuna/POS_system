# Generated by Django 4.2.10 on 2024-03-13 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_category_alter_client_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('EN_VENTE', 'En vente'), ('EN_RÉPARATION', 'En réparation')], default='EN_VENTE', max_length=20),
        ),
    ]
