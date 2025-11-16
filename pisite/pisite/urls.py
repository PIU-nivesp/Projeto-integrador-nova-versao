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

    # ----------------------------------------------------
    # URLs da Aplicação 'catalogo'
    # ----------------------------------------------------
    
    # Rota raiz: Mapeada para o login, nomeada como 'login' para redirecionamentos.
    path('', views.login_view, name='login'),
    
    # Rota para a página de Cadastro de Usuário
    path('cadastro', views.cadastro_view, name='cadastro'),
    
    # Rota para a página principal (Home)
    path('home', views.index, name='index'),
    
    # Rota para a página de estoque
    path('estoque', views.estoque, name='estoque'),
    
    # Rota para a página de inserção de dados
    path('inserir', views.inserir, name='inserir'),

    # Rota para processar o cadastro de medicamento (POST/AJAX)
    path('cadastro_medicamento', views.cadastro_medicamento, name='cadastro_medicamento'),
    
    # NOVO: Rota para processar a entrada de novo lote (POST/AJAX)
    path('entrada_lote', views.entrada_lote, name='entrada_lote'),
    
    # NOVO: Rota API para buscar medicamentos (GET/AJAX). Usamos 'api/' para organizar.
    path('api/medicamentos', views.carregar_medicamentos, name='api_medicamentos'),
    
    # Rota para o logout (limpa a sessão)
    path('logout', views.logout_view, name='logout'),
]