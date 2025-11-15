from django.shortcuts import render, redirect
from .models import Usuarios  # Importa o modelo de usuários que contém o hash
import hashlib  # Módulo para calcular o hash SHA-256

# View para a página de login
def login_view(request):
    # O erro_aqui foi removido.
    if request.method == 'POST':
        # 1. Obter dados do formulário (que usa 'username' e 'password')
        email_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')

        # 2. Calcular o hash SHA-256 da senha digitada
        senha_hash_fornecida = hashlib.sha256(senha_digitada.encode('utf-8')).hexdigest()

        # REMOVA ESTES PRINTS APÓS CONFIRMAR QUE TUDO FUNCIONA
        #print("\n------------------- DEBUG LOGIN -------------------")
        #print(f"1. E-mail digitado: {email_digitado}")
        #print(f"2. Hash fornecido (Calculado do input): {senha_hash_fornecida}")

        try:
            # 3. Buscar o usuário pelo email
            usuario = Usuarios.objects.get(email=email_digitado)

            # REMOVA ESTES PRINTS APÓS CONFIRMAR QUE TUDO FUNCIONA
            #print(f"3. Usuário encontrado: {usuario.email}")
            #print(f"4. Hash NO BANCO DE DADOS: {usuario.senha_hash}")
            
            # 4. Comparar os hashes
            if usuario.senha_hash == senha_hash_fornecida:
                
                # ✅ SUCESSO! IMPLEMENTAÇÃO DA SESSÃO
                request.session['usuario_id'] = usuario.id
                request.session['usuario_email'] = usuario.email
                
                print("5. RESULTADO: SUCESSO! HASHES SÃO IGUAIS.")
                return redirect('index') 
            else:
                # Senha incorreta
                print("5. RESULTADO: FALHA! HASHES SÃO DIFERENTES.")
                context = {'error': 'E-mail ou senha inválidos.'}
                return render(request, 'catalogo/login.html', context)

        except Usuarios.DoesNotExist:
            # Usuário não encontrado
            context = {'error': 'E-mail ou senha inválidos.'}
            return render(request, 'catalogo/login.html', context)

    # Para o método GET
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
    try:
        del request.session['usuario_id']
        del request.session['usuario_email']
    except KeyError:
        # Não há problema se a chave já não existir
        pass
        
    return redirect('login') # Redireciona para a página de login