# Generated by Django 4.2.10 on 2024-04-02 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorderitem',
            old_name='order',
            new_name='purchase_order',
        ),
        migrations.AlterUniqueTogether(
            name='purchaseorderitem',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='saleitem',
            unique_together=set(),
        ),
    ]
