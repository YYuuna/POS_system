from django.urls import path
from . import views

urlpatterns = [
path('login/',views.UserLoginView.as_view(),name='login'),
    path('ajouter-client/', views.AddClientView.as_view(), name='add-client'),
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('client/<int:pk>/modifier', views.ClientUpdateView.as_view(), name='update-client'),
    path('client/<int:pk>/supprimer', views.ClientDeleteView.as_view(), name='delete-client'),
    path('ajouter-fournisseur/', views.AddSupplierView.as_view(), name='add-supplier'),
    path('fournisseurs/', views.SupplierListView.as_view(), name='supplier-list'),
    path('fournisseur/<int:pk>/modifier', views.SupplierUpdateView.as_view(), name='update-supplier'),
    path('fournisseur/<int:pk>/supprimer', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('ajouter-produit/', views.AddProductView.as_view(), name='add-product'),
    path('produits/', views.ProductListView.as_view(), name='product-list'),
    path('comptes/', views.AccountListView.as_view(), name='account-list'),
    path('employes/', views.EmployeeListView.as_view(), name='employee-list'),
    path('commandes', views.PurchaseOrderListView.as_view(), name='purchase-order-list'),
    path('ventes', views.SaleListView.as_view(), name='sale-list'),
    path('stock', views.ProductListView.as_view(), name='products-list'),
    path('reparations', views.RepairListView.as_view(), name='repair-list'),
]