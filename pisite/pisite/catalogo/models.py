from django.db import models
from django.utils import timezone 

# --- Definições de Choices (substituindo ENUM) ---

CARGO_CHOICES = (
    ('farmaceutico', 'Farmacêutico'),
    ('admin', 'Administrador'),
    ('tecnico', 'Técnico'),
)

UNIDADE_CHOICES = (
    ('comprimido', 'Comprimido'),
    ('ml', 'Mililitro'),
    ('mg', 'Miligrama'),
    ('unidade', 'Unidade'),
)

TIPO_MOVIMENTACAO_CHOICES = (
    ('entrada', 'Entrada'),
    ('saida', 'Saída'),
)

PERIODO_CHOICES = (
    ('diario', 'Diário'),
    ('semanal', 'Semanal'),
    ('mensal', 'Mensal'),
)

# Choices para Forma Farmacêutica
FORMA_CHOICES = (
    ('comprimido', 'Comprimido'),
    ('capsula', 'Cápsula'),
    ('solucao', 'Solução'),
    ('injetavel', 'Injetável'),
    ('pomada', 'Pomada'),
)

# -------------------------------------------------

## Tabela usuarios
class Usuarios(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    senha_hash = models.CharField(max_length=255)
    cargo = models.CharField(max_length=15, choices=CARGO_CHOICES)
    criado_em = models.DateTimeField() 

    def __str__(self):
        return self.nome
        
    class Meta:
        db_table = 'usuarios'
        verbose_name_plural = 'Usuários'

## Tabela medicamentos (CORRIGIDA)
class Medicamentos(models.Model):
    # CAMPOS QUE ESTAVAM FALTANDO (CAUSANDO O ERRO)
    nome_comercial = models.CharField(max_length=150) 
    principio_ativo = models.CharField(max_length=150, null=True, blank=True) 
    concentracao = models.CharField(max_length=50, null=True, blank=True) 
    forma_farmaceutica = models.CharField(max_length=50, choices=FORMA_CHOICES, default='comprimido') 
    controlado = models.BooleanField(default=False) 
    
    # Campos ajustados/mantidos
    descricao = models.TextField(null=True, blank=True)
    codigo_barras = models.CharField(max_length=80, unique=True, null=True, blank=True)
    fabricante = models.CharField(max_length=100, null=True, blank=True) 
    lote = models.CharField(max_length=200, null=True, blank=True) 
    validade = models.DateField(null=True, blank=True) 
    
    unidade_medida = models.CharField(max_length=15, choices=UNIDADE_CHOICES)
    criado_em = models.DateTimeField() 
    imagem = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.nome_comercial} ({self.concentracao or 'N/A'})"

    class Meta:
        db_table = 'medicamentos'
        verbose_name_plural = 'Medicamentos'

## Tabela fornecedores
class Fornecedores(models.Model):
    nome = models.CharField(max_length=150)
    contato = models.CharField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField() 

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'fornecedores'
        verbose_name_plural = 'Fornecedores'

## Tabela receitas
class Receitas(models.Model):
    paciente_nome = models.CharField(max_length=150)
    medico_nome = models.CharField(max_length=150)
    crm_medico = models.CharField(max_length=20)
    data_prescricao = models.DateField()
    observacao = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField()

    def __str__(self):
        return f"Receita de {self.paciente_nome}"

    class Meta:
        db_table = 'receitas'
        verbose_name_plural = 'Receitas'


## Tabela estoque 
class Estoque(models.Model):
    medicamento = models.ForeignKey(Medicamentos, on_delete=models.CASCADE) 
    quantidade = models.IntegerField()
    alerta_minimo = models.IntegerField(default=10)
    atualizado_em = models.DateTimeField() 

    class Meta:
        db_table = 'estoque'
        verbose_name_plural = 'Estoque'


## Tabela movimentacoes
class Movimentacoes(models.Model):
    medicamento = models.ForeignKey(Medicamentos, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True) 
    receita = models.ForeignKey(Receitas, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO_CHOICES)
    quantidade = models.IntegerField()
    data_movimentacao = models.DateTimeField()
    observacao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'movimentacoes'
        verbose_name_plural = 'Movimentações'

## Tabela versoes
class Versoes(models.Model):
    tabela_afetada = models.CharField(max_length=50)
    registro_id = models.IntegerField()
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    alteracao = models.TextField()
    data_alteracao = models.DateTimeField()

    class Meta:
        db_table = 'versoes'
        verbose_name_plural = 'Versões'

## Tabela consumo
class Consumo(models.Model):
    medicamento = models.ForeignKey(Medicamentos, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES)
    quantidade_consumida = models.IntegerField()
    receita = models.ForeignKey(Receitas, on_delete=models.SET_NULL, null=True, blank=True)
    data_registro = models.DateTimeField()

    class Meta:
        db_table = 'consumo'
        verbose_name_plural = 'Consumo'