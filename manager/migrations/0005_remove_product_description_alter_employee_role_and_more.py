# Generated by Django 4.2.10 on 2024-03-24 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_remove_product_status_remove_repair_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Employé', 'Employé')], db_column='Rôle', default='Employé', max_length=100, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='product',
            name='state',
            field=models.CharField(choices=[('En vente', 'En vente'), ('En réparation', 'En réparation')], db_column='État', default='EN_VENTE', max_length=20),
        ),
    ]
