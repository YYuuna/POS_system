from django.urls import path
from . import views

urlpatterns = [
    path('ajouter-client', views.AddClientView.as_view(), name='add-client'),
    path('login',views.UserLoginView.as_view(),name='login'),
    path('clients/', views.ClientListView.as_view(), name='client-list'),
   
]