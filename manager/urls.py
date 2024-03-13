from django.urls import path
from . import views

urlpatterns = [
path('login/',views.UserLoginView.as_view(),name='login'),
    path('ajouter-client/', views.AddClientView.as_view(), name='add-client'),
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('modifier-client/<int:pk>/', views.ClientUpdateView.as_view(), name='update-client'),
    path('supprimer-client/<int:pk>/', views.ClientDeleteView.as_view(), name='delete-client'),
    path('ajouter-fournisseur/', views.AddSupplierView.as_view(), name='add-supplier'),
    path('fournisseurs/', views.SupplierListView.as_view(), name='supplier-list'),
    path('modifier-fournisseur/<int:pk>/', views.SupplierUpdateView.as_view(), name='update-supplier'),
    path('supprimer-fournisseur/<int:pk>/', views.SupplierDeleteView.as_view(), name='delete-supplier'),
]