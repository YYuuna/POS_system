# Generated by Django 4.2.10 on 2024-03-20 13:37

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_alter_product_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='status',
        ),
        migrations.RemoveField(
            model_name='repair',
            name='status',
        ),
        migrations.AddField(
            model_name='product',
            name='state',
            field=models.CharField(choices=[('EN_VENTE', 'En vente'), ('EN_RÉPARATION', 'En réparation')], db_column='État', default='EN_VENTE', max_length=20),
        ),
        migrations.AddField(
            model_name='repair',
            name='state',
            field=models.CharField(choices=[('EN_COURS', 'En cours'), ('TERMINÉ', 'Terminé')], db_column='État', default='EN_COURS', max_length=20),
        ),
        migrations.AlterField(
            model_name='account',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, db_column="Date d'adhésion", verbose_name='Date joined'),
        ),
        migrations.AlterField(
            model_name='account',
            name='employee',
            field=models.OneToOneField(blank=True, db_column='Employé', null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.employee'),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(db_column='Actif', default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(db_column='Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_column='Nom', max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.TextField(db_column='Adresse'),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(db_column='Email', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(db_column='Prénom', max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(db_column='Nom', max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(db_column='Téléphone', max_length=128, region='DZ', unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.TextField(db_column='Adresse'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(db_column='Email', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(db_column='Prénom', max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(db_column='Nom', max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(db_column='Téléphone', max_length=128, region='DZ', unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('EMPLOYEE', 'Employee')], db_column='Rôle', default='EMPOYEE', max_length=100, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(blank=True, db_column='Salaire', decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(db_column='Catégorie', default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='manager.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(db_column='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='initial_buying_price',
            field=models.DecimalField(blank=True, db_column="Prix d'achat initiale", decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='initial_selling_price',
            field=models.DecimalField(blank=True, db_column='Prix de vente initiale', decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_column='Nom', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, db_column='Quantité', default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(blank=True, db_column='Fournisseur', null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager.supplier'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateField(blank=True, db_column='Date de livraison', null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='is_delivered',
            field=models.BooleanField(db_column='Est livré', default=False),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateField(auto_now_add=True, db_column='Date de commande'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(blank=True, db_column='Fournisseur', null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager.supplier'),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='order',
            field=models.ForeignKey(db_column='Commande', on_delete=django.db.models.deletion.CASCADE, to='manager.purchaseorder'),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='product',
            field=models.ForeignKey(db_column='Produit', on_delete=django.db.models.deletion.CASCADE, to='manager.product'),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='purchase_price',
            field=models.DecimalField(db_column="Prix d'achat", decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='quantity',
            field=models.IntegerField(db_column='Quantité'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='client',
            field=models.ForeignKey(blank=True, db_column='Client', null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager.client'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='description',
            field=models.TextField(db_column='Description'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='product',
            field=models.ForeignKey(blank=True, db_column='Produit', null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager.product'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='repair_date',
            field=models.DateField(auto_now_add=True, db_column='Date de réparation'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='client',
            field=models.ForeignKey(blank=True, db_column='Client', null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager.client'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_date',
            field=models.DateField(auto_now_add=True, db_column='Date de vente'),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='product',
            field=models.ForeignKey(db_column='Produit', on_delete=django.db.models.deletion.CASCADE, to='manager.product'),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='quantity',
            field=models.IntegerField(db_column='Quantité'),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='sale',
            field=models.ForeignKey(db_column='Vente', on_delete=django.db.models.deletion.CASCADE, to='manager.sale'),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='sale_price',
            field=models.DecimalField(db_column='Prix de vente', decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.TextField(db_column='Adresse'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.EmailField(db_column='Email', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(db_column='Nom', max_length=100),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(db_column='Téléphone', max_length=128, region='DZ', unique=True),
        ),
        migrations.AlterModelTable(
            name='account',
            table='Compte',
        ),
        migrations.AlterModelTable(
            name='category',
            table='Catégorie',
        ),
        migrations.AlterModelTable(
            name='client',
            table='Client',
        ),
        migrations.AlterModelTable(
            name='employee',
            table='Employé',
        ),
        migrations.AlterModelTable(
            name='product',
            table='Produit',
        ),
        migrations.AlterModelTable(
            name='purchaseorder',
            table='Commande',
        ),
        migrations.AlterModelTable(
            name='purchaseorderitem',
            table='ArticleCommande',
        ),
        migrations.AlterModelTable(
            name='repair',
            table='Réparation',
        ),
        migrations.AlterModelTable(
            name='sale',
            table='Vente',
        ),
        migrations.AlterModelTable(
            name='saleitem',
            table='ArticleVente',
        ),
        migrations.AlterModelTable(
            name='supplier',
            table='Fournisseur',
        ),
    ]
