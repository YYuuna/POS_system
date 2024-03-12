from django.urls import path
from . import views

urlpatterns = [
    path('ajouter-client', views.AddClientView.as_view(), name='add-client'),
    path('login',views.UserLoginView.as_view(),name='login'),
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('ajouter-fournisseur', views.AddSupplierView.as_view(), name='add-supplier'),
    path('modifier-client/<int:pk>/', views.ClientUpdateView.as_view(), name='update-client'),
    path('supprimer-client/<int:pk>/', views.ClientDeleteView.as_view(), name='delete-client'),

   
]