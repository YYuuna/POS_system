from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('produit/<int:pk>/modifier', views.ProductUpdateView.as_view(), name='update-product'),
    path('produit/<int:pk>/supprimer', views.ProductDeleteView.as_view(), name='delete-product'),
    path('produit/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('ajouter-categorie/', views.AddCategoryView.as_view(), name='add-category'),
    path('comptes/', views.AccountListView.as_view(), name='account-list'),
    path('ajouter-compte/', views.AddAccountView.as_view(), name='add-account'),
    path('compte/<int:pk>/changer-mot-de-passe/', views.AccountUpdateView.as_view(), name='update-account'),
    path('compte/<int:pk>/supprimer/', views.AccountDeleteView.as_view(), name='delete-account'),
    path('employes/', views.EmployeeListView.as_view(), name='employee-list'),
    path('ajouter-employe/',views.AddEmployeeView.as_view(),name='add-employee'),
    path('employe/<int:pk>/modifier/',views.EmployeeUpdateView.as_view(),name='update-employee'),
    path('employe/<int:pk>/supprimer/',views.EmployeeDeleteView.as_view(),name='delete-employee'),
    path('commandes/', views.PurchaseOrderListView.as_view(), name='purchase-order-list'),
    path('ajouter-commande/', views.AddPurchaseOrderView.as_view(), name='add-purchase-order'),
    path('commande/<int:pk>/', views.PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    path('commande/<int:pk>/modifier/', views.PurchaseOrderUpdateView.as_view(), name='update-purchase-order'),
    path('commande/<int:pk>/supprimer/', views.PurchaseOrderDeleteView.as_view(), name='delete-purchase-order'),
    path('commande/<int:pk>/livrer/', views.PurchaseOrderDeliverView.as_view(), name='deliver-purchase-order'),
    path('ventes/', views.SaleListView.as_view(), name='sale-list'),
    path('ajouter-vente/', views.AddSaleView.as_view(), name='add-sale'),
    path('vente/<int:pk>/', views.SaleDetailView.as_view(), name='sale-detail'),
    path('vente/<int:pk>/modifier/', views.SaleUpdateView.as_view(), name='update-sale'),
    path('vente/<int:pk>/annuler/', views.SaleCancelView.as_view(), name='cancel-sale'),
    path('vente/<int:pk>/facture/', views.SaleInvoiceView.as_view(), name='sale-invoice'),
    path('produit/<int:pk>/prix_vente_initial/', views.ProductInitialSellingPriceView.as_view(), name='initial-sale-price'),
    path('produit/<int:pk>/prix_achat_initial/', views.ProductInitialPurchasePriceView.as_view(), name='initial-purchase-price'),
    path('stock/', views.ProductListView.as_view(), name='products-list'),
    path('reparations/', views.RepairListView.as_view(), name='repair-list'),
    path('ajouter-reparation/', views.AddRepairView.as_view(), name='add-repair'),
    path('reparation/<int:pk>/', views.RepairDetailView.as_view(), name='repair-detail'),
    path('reparation/<int:pk>/modifier/', views.RepairUpdateView.as_view(), name='update-repair'),
    path('reparation/<int:pk>/supprimer/', views.RepairDeleteView.as_view(), name='delete-repair'),
    path('reparation/<int:pk>/terminer/', views.RepairFinishView.as_view(), name='finish-repair'),
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('test/', views.TestView.as_view(), name='test'),
]