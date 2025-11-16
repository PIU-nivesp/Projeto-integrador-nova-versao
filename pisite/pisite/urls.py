"""
URL configuration for pisite project.

The `urlpatterns` list routes URLs to views.
For more information, see: https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from pisite.catalogo import views

urlpatterns = [
    # URLs do Django Admin
    path('admin/', admin.site.urls),

    # URLs da Aplicação 'catalogo'
    
    # Rota raiz: Mapeada para o login, NOME CORRIGIDO para 'login_view'.
    path('', views.login_view, name='login_view'),
    
    # NOVO: Rota para a página de Cadastro
    path('cadastro', views.cadastro_view, name='cadastro'),
    
    # Rota para a página principal (Home)
    path('home', views.index, name='index'),
    
    # Rota para a página de estoque
    path('estoque', views.estoque, name='estoque'),
    
    # Rota para a página de inserção de dados
    path('inserir', views.inserir, name='inserir'),

    # Rota para o logout (limpa a sessão)
    path('logout', views.logout_view, name='logout'),
]