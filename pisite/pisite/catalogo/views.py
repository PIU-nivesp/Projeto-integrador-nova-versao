from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse 
from django.views.decorators.http import require_POST 
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.utils import timezone 
from datetime import datetime
# Garanta que Movimentacoes está na sua importação das models
from .models import Usuarios, Medicamentos, Estoque, Movimentacoes 

# ----------------------------------------------------
# Funções de Autenticação
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
# Função de Cadastro de Usuário
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
                # CORRIGIDO: Usando timezone.now() que é compatível com o Django
                criado_em=timezone.now() 
            )
            
            # 6. Adicionar mensagem de sucesso e redirecionar para o login
            messages.success(request, f'Usuário {nome} cadastrado com sucesso! Faça login abaixo.')
            # CORREÇÃO APLICADA AQUI:
            return redirect('login') 
            
        except Exception as e:
            print(f"Erro ao salvar usuário: {e}")
            messages.error(request, 'Erro interno ao finalizar cadastro. Tente novamente.')
            return render(request, 'catalogo/cadastro.html')
        
    return render(request, 'catalogo/cadastro.html')


# ----------------------------------------------------
# Função de Cadastro de Medicamento
# ----------------------------------------------------

@require_POST
def cadastro_medicamento(request):
    """
    Lida com o processamento da submissão do formulário de Cadastro de Novo Medicamento 
    e salva os dados nas tabelas Medicamentos e Estoque.
    """
    # Checagem de Sessão (Importante para proteger a rota de POST)
    if 'usuario_id' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Acesso negado. Sessão expirada.'}, status=401)
        
    try:
        nome_comercial = request.POST.get('nome_comercial')
        principio_ativo = request.POST.get('principio_ativo')
        concentracao = request.POST.get('concentracao')
        forma_farmaceutica = request.POST.get('forma_farmaceutica')
        unidade_medida = request.POST.get('unidade_medida')
        estoque_minimo = request.POST.get('estoque_minimo', 10)
        controlado = request.POST.get('controlado') == 'on' 

        # 1. Cria o registro base do medicamento
        medicamento = Medicamentos.objects.create(
            nome_comercial=nome_comercial,
            principio_ativo=principio_ativo,
            concentracao=concentracao,
            forma_farmaceutica=forma_farmaceutica,
            unidade_medida=unidade_medida,
            controlado=controlado,
            criado_em=timezone.now(),
        )
        
        # 2. Cria o registro de estoque
        Estoque.objects.create(
            medicamento=medicamento,
            quantidade=0, 
            alerta_minimo=int(estoque_minimo),
            atualizado_em=timezone.now()
        )

        return JsonResponse({'status': 'success', 'message': f'Medicamento "{nome_comercial}" cadastrado com sucesso!'})

    except Exception as e:
        print(f"Erro no cadastro de medicamento: {e}")
        return JsonResponse({'status': 'error', 'message': f'Erro ao cadastrar: {str(e)}'}, status=400)


# ----------------------------------------------------
# API: Carregar Lista de Medicamentos
# ----------------------------------------------------

def carregar_medicamentos(request):
    """Retorna uma lista de medicamentos cadastrados em formato JSON."""
    if 'usuario_id' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Acesso negado.'}, status=401)
        
    try:
        # Busca todos os medicamentos
        medicamentos = Medicamentos.objects.all().order_by('nome_comercial')
        
        # Formata os dados para JSON
        lista_medicamentos = [
            {
                'id': med.id,
                # Combina nome comercial e concentração para melhor exibição
                'nome': f"{med.nome_comercial} ({med.concentracao or 'S/C'})", 
            }
            for med in medicamentos
        ]
        
        return JsonResponse({'status': 'success', 'medicamentos': lista_medicamentos})
    
    except Exception as e:
        print(f"Erro ao carregar medicamentos: {e}")
        return JsonResponse({'status': 'error', 'message': 'Erro ao buscar lista de medicamentos.'}, status=500)


# ----------------------------------------------------
# API: Entrada de Novo Lote
# ----------------------------------------------------

@require_POST
def entrada_lote(request):
    """
    Processa a entrada de um novo lote: atualiza o estoque e registra a movimentação.
    """
    if 'usuario_id' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Acesso negado. Sessão expirada.'}, status=401)
        
    try:
        # Dados do formulário
        medicamento_id = request.POST.get('medicamento_lote')
        numero_lote = request.POST.get('numero_lote')
        quantidade = int(request.POST.get('quantidade_lote'))
        data_vencimento_str = request.POST.get('data_vencimento')
        
        # Busca objetos
        medicamento = get_object_or_404(Medicamentos, pk=medicamento_id)
        estoque_item = get_object_or_404(Estoque, medicamento=medicamento)
        usuario_responsavel = get_object_or_404(Usuarios, pk=request.session['usuario_id'])

        # 1. Conversão de Data
        data_vencimento = datetime.strptime(data_vencimento_str, '%Y-%m-%d').date()

        # 2. Atualiza o registro principal do Medicamento (com o lote mais recente)
        medicamento.lote = numero_lote
        medicamento.validade = data_vencimento
        medicamento.save()
        
        # 3. Atualiza o Estoque: Incrementa a quantidade
        estoque_item.quantidade += quantidade
        estoque_item.atualizado_em = timezone.now()
        estoque_item.save()
        
        # 4. Cria o registro de Movimentação (tipo 'entrada')
        Movimentacoes.objects.create(
            medicamento=medicamento,
            usuario=usuario_responsavel,
            tipo='entrada',
            quantidade=quantidade,
            data_movimentacao=timezone.now(),
            observacao=f"Entrada de novo Lote: {numero_lote}. Vencimento: {data_vencimento_str}"
        )

        return JsonResponse({'status': 'success', 'message': f'{quantidade} unidades do lote "{numero_lote}" de {medicamento.nome_comercial} adicionadas ao estoque.'})

    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'A quantidade ou ID do medicamento são inválidos.'}, status=400)
    except Exception as e:
        print(f"Erro na entrada de lote: {e}")
        return JsonResponse({'status': 'error', 'message': f'Erro ao registrar entrada: {str(e)}'}, status=400)


# ----------------------------------------------------
# Funções de Navegação (PROTEGIDAS)
# ----------------------------------------------------

def index(request):
    # CHECAGEM DE SESSÃO
    if 'usuario_id' not in request.session:
        # CORREÇÃO APLICADA AQUI:
        return redirect('login') 
        
    return render(request, 'catalogo/index.html')

def estoque(request):
    # CHECAGEM DE SESSÃO
    if 'usuario_id' not in request.session:
        # CORREÇÃO APLICADA AQUI:
        return redirect('login')
        
    return render(request, 'catalogo/estoque.html')

def inserir(request):
    # CHECAGEM DE SESSÃO
    if 'usuario_id' not in request.session:
        # CORREÇÃO APLICADA AQUI:
        return redirect('login') 
        
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
        
    # CORREÇÃO APLICADA AQUI:
    return redirect('login')