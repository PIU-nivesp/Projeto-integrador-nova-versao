from django.shortcuts import render, redirect
from .models import Usuarios  # Importa o modelo de usuários que contém o hash
from django.contrib.auth.hashers import check_password # <-- NOVO: Importe a função de checagem do Django
# import hashlib  # <-- REMOVA esta linha (ou comente-a)

# View para a página de login
def login_view(request):
    if request.method == 'POST':
        # 1. Obter dados do formulário (o campo é 'username', mas você está usando para e-mail)
        email_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')

        # Contexto de erro padrão para reutilização
        context = {'error': 'E-mail ou senha inválidos.'}
        
        # Se algum campo estiver vazio, retorna erro imediatamente
        if not email_digitado or not senha_digitada:
            return render(request, 'catalogo/login.html', context)


        # 2. Calcular o hash SHA-256 da senha digitada
        # IMPORTANTE: Garanta que a senha no banco foi criada exatamente com o mesmo hash!
        #senha_hash_fornecida = hashlib.sha256(senha_digitada.encode('utf-8')).hexdigest()

        try:
            # 3. Buscar o usuário pelo email
            usuario = Usuarios.objects.get(email=email_digitado)

            # 4. Comparar os hashes
            if check_password(senha_digitada, usuario.senha_hash):
                
                # ✅ SUCESSO! IMPLEMENTAÇÃO DA SESSÃO
                request.session['usuario_id'] = usuario.id
                request.session['usuario_email'] = usuario.email
                
                print("5. RESULTADO: SUCESSO! HASHES SÃO IGUAIS.")
                return redirect('index') 
            else:
                # Senha incorreta
                print("5. RESULTADO: FALHA! HASHES SÃO DIFERENTES.")
                return render(request, 'catalogo/login.html', context)

        except Usuarios.DoesNotExist:
            # Usuário não encontrado
            return render(request, 'catalogo/login.html', context)

    # Para o método GET (primeiro acesso)
    return render(request, 'catalogo/login.html')

# ----------------------------------------------------
# Funções de Navegação (PROTEGIDAS)
# ----------------------------------------------------

def index(request):
    # CHECAGEM DE SESSÃO: Se não estiver logado, redireciona para o login
    if 'usuario_id' not in request.session:
        return redirect('login') 
        
    return render(request, 'catalogo/index.html')

def estoque(request):
    # CHECAGEM DE SESSÃO: Se não estiver logado, redireciona para o login
    if 'usuario_id' not in request.session:
        return redirect('login')
        
    return render(request, 'catalogo/estoque.html')

def inserir(request):
    # CHECAGEM DE SESSÃO: Se não estiver logado, redireciona para o login
    if 'usuario_id' not in request.session:
        return redirect('login') 
        
    return render(request, 'catalogo/inserir.html')

# ----------------------------------------------------
# Função de Logout
# ----------------------------------------------------

def logout_view(request):
    """Limpa a sessão do usuário e o redireciona para a página de login."""
    # Garante que as chaves sejam excluídas com segurança se existirem
    request.session.pop('usuario_id', None)
    request.session.pop('usuario_email', None)
        
    return redirect('login') # Redireciona para a página de login