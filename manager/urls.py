from django.urls import path
from . import views
from .views import ProductDetailView

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
    path('produit/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
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
    path('ventes/', views.SaleListView.as_view(), name='sale-list'),
    path('stock/', views.ProductListView.as_view(), name='products-list'),
    path('reparations/', views.RepairListView.as_view(), name='repair-list'),
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
]