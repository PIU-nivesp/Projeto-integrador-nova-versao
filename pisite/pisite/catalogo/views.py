from django.shortcuts import render, redirect
from .models import Usuarios
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages # Importação crucial para mensagens de sucesso/erro
from datetime import datetime # Necessário para preencher o campo 'criado_em' do modelo Usuarios


# ----------------------------------------------------
# View para a página de login
# ----------------------------------------------------

def login_view(request):
    """
    Lida com o login do usuário, autenticando contra o modelo Usuarios
    e criando a sessão nativa do Django.
    """
    
    # Se o usuário já estiver logado, redireciona para a home
    if 'usuario_id' in request.session:
        return redirect('index')

    if request.method == 'POST':
        # 1. Obter dados do formulário
        email_digitado = request.POST.get('email')
        senha_digitada = request.POST.get('password')

        # Se faltar campo, exibe erro
        if not email_digitado or not senha_digitada:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'catalogo/login.html') 
        
        try:
            # 2. Buscar o usuário pelo email no banco de dados
            usuario = Usuarios.objects.get(email=email_digitado)

            # 3. Comparar o hash da senha usando o check_password do Django
            if check_password(senha_digitada, usuario.senha_hash):
                
                # SUCESSO! Criação da sessão nativa do Django
                # Armazenar ID, Email e Cargo (útil para uso posterior nos templates)
                request.session['usuario_id'] = usuario.id
                request.session['usuario_email'] = usuario.email
                request.session['usuario_nome'] = usuario.nome
                request.session['usuario_cargo'] = usuario.cargo
                
                print("5. RESULTADO: SUCESSO! Login Django OK.")
                return redirect('index') 
            else:
                # Senha incorreta
                messages.error(request, 'E-mail ou senha inválidos. Tente novamente.')
                print("5. RESULTADO: FALHA! Senha Django Incorreta.")
                return render(request, 'catalogo/login.html')

        except Usuarios.DoesNotExist:
            # Usuário não encontrado
            messages.error(request, 'E-mail ou senha inválidos. Tente novamente.')
            return render(request, 'catalogo/login.html')
        
        except Exception as e:
            # Erro genérico
            print(f"Erro de login: {e}")
            messages.error(request, 'Ocorreu um erro interno. Tente novamente.')
            return render(request, 'catalogo/login.html')
        
    # Para o método GET (primeiro acesso)
    return render(request, 'catalogo/login.html')


# ----------------------------------------------------
# Função de Cadastro
# ----------------------------------------------------

def cadastro_view(request):
    """Lida com a criação de novos usuários no banco de dados local."""
    
    if request.method == 'POST':
        # 1. Obter dados do formulário de cadastro
        nome = request.POST.get('cadNome')
        email = request.POST.get('cadEmail')
        senha = request.POST.get('cadSenha')
        cargo = request.POST.get('cadCargo')
        
        # 2. Validações básicas
        if not nome or not email or not senha or not cargo:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'catalogo/cadastro.html')

        # 3. Validação de e-mail duplicado
        if Usuarios.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está em uso. Tente outro.')
            return render(request, 'catalogo/cadastro.html')
        
        try:
            # 4. Criar o hash da senha (essencial para segurança)
            senha_hash = make_password(senha)
            
            # 5. Criar e salvar o novo usuário no banco de dados
            Usuarios.objects.create(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                cargo=cargo,
                # O CAMPO 'criado_em' DEVE SER PREENCHIDO (usamos a hora atual)
                criado_em=datetime.now() 
            )
            
            # 6. Adicionar mensagem de sucesso e redirecionar para o login
            messages.success(request, f'Usuário {nome} cadastrado com sucesso! Faça login abaixo.')
            # CORRIGIDO o nome da rota de redirect, conforme urls.py
            return redirect('login_view') 
            
        except Exception as e:
            print(f"Erro ao salvar usuário: {e}")
            messages.error(request, 'Erro interno ao finalizar cadastro. Tente novamente.')
            return render(request, 'catalogo/cadastro.html')
        
    return render(request, 'catalogo/cadastro.html')


# ----------------------------------------------------
# Funções de Navegação (PROTEGIDAS)
# ----------------------------------------------------

def index(request):
    # CHECAGEM DE SESSÃO: Se não estiver logado, redireciona para o login
    if 'usuario_id' not in request.session:
        # CORRIGIDO o nome da rota de redirect, conforme urls.py
        return redirect('login_view') 
        
    return render(request, 'catalogo/index.html')

def estoque(request):
    # CHECAGEM DE SESSÃO: Se não estiver logado, redireciona para o login
    if 'usuario_id' not in request.session:
        # CORRIGIDO o nome da rota de redirect, conforme urls.py
        return redirect('login_view')
        
    return render(request, 'catalogo/estoque.html')

def inserir(request):
    # CHECAGEM DE SESSÃO: Se não estiver logado, redireciona para o login
    if 'usuario_id' not in request.session:
        # CORRIGIDO o nome da rota de redirect, conforme urls.py
        return redirect('login_view') 
        
    return render(request, 'catalogo/inserir.html')

# ----------------------------------------------------
# Função de Logout
# ----------------------------------------------------

def logout_view(request):
    """Limpa a sessão do usuário e o redireciona para a página de login."""
    # Remove as chaves de sessão
    request.session.pop('usuario_id', None)
    request.session.pop('usuario_email', None)
    request.session.pop('usuario_nome', None)
    request.session.pop('usuario_cargo', None)
        
    # CORRIGIDO o nome da rota de redirect, conforme urls.py
    return redirect('login_view')