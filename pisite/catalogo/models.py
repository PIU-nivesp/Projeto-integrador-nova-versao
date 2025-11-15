from django.db import models

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

# -------------------------------------------------

## Tabela usuarios
class Usuarios(models.Model):
    # O campo 'id' (INT PRIMARY KEY AUTO_INCREMENT) é criado automaticamente pelo Django
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    senha_hash = models.CharField(max_length=255)
    cargo = models.CharField(max_length=15, choices=CARGO_CHOICES)
    # CORRIGIDO: Removido auto_now_add=True para permitir carregamento via fixture
    criado_em = models.DateTimeField() 

    def __str__(self):
        return self.nome
        
    class Meta:
        db_table = 'usuarios'
        verbose_name_plural = 'Usuários'

## Tabela medicamentos
class Medicamentos(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(null=True, blank=True)
    codigo_barras = models.CharField(max_length=80, unique=True, null=True, blank=True)
    fabricante = models.CharField(max_length=100)
    lote = models.CharField(max_length=200)
    validade = models.DateField()
    unidade_medida = models.CharField(max_length=15, choices=UNIDADE_CHOICES)
    # ESTA É A CORREÇÃO CRÍTICA:
    criado_em = models.DateTimeField() 
    imagem = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nome

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
    # CORRIGIDO: Removido auto_now_add=True para permitir carregamento via fixture
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
    # CORRIGIDO: Removido auto_now_add=True para permitir carregamento via fixture
    criado_em = models.DateTimeField()

    def __str__(self):
        return f"Receita de {self.paciente_nome}"

    class Meta:
        db_table = 'receitas'
        verbose_name_plural = 'Receitas'


## Tabela estoque
class Estoque(models.Model):
    # FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id) ON DELETE CASCADE
    medicamento = models.ForeignKey(Medicamentos, on_delete=models.CASCADE) 
    quantidade = models.IntegerField()
    alerta_minimo = models.IntegerField(default=10)
    # CORRIGIDO: Removido auto_now=True para permitir carregamento via fixture
    atualizado_em = models.DateTimeField() 

    class Meta:
        db_table = 'estoque'
        verbose_name_plural = 'Estoque'


## Tabela movimentacoes
class Movimentacoes(models.Model):
    # FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id) ON DELETE CASCADE
    medicamento = models.ForeignKey(Medicamentos, on_delete=models.CASCADE)
    # FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True) 
    # FOREIGN KEY (receita_id) REFERENCES receitas(id) ON DELETE SET NULL
    receita = models.ForeignKey(Receitas, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO_CHOICES)
    quantidade = models.IntegerField()
    # CORRIGIDO: Removido auto_now_add=True para permitir carregamento via fixture
    data_movimentacao = models.DateTimeField()
    observacao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'movimentacoes'
        verbose_name_plural = 'Movimentações'

## Tabela versoes
class Versoes(models.Model):
    tabela_afetada = models.CharField(max_length=50)
    registro_id = models.IntegerField()
    # FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    alteracao = models.TextField()
    # CORRIGIDO: Removido auto_now_add=True para permitir carregamento via fixture
    data_alteracao = models.DateTimeField()

    class Meta:
        db_table = 'versoes'
        verbose_name_plural = 'Versões'

## Tabela consumo
class Consumo(models.Model):
    # FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id) ON DELETE CASCADE
    medicamento = models.ForeignKey(Medicamentos, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES)
    quantidade_consumida = models.IntegerField()
    # FOREIGN KEY (receita_id) REFERENCES receitas(id) ON DELETE SET NULL
    receita = models.ForeignKey(Receitas, on_delete=models.SET_NULL, null=True, blank=True)
    # CORRIGIDO: Removido auto_now_add=True para permitir carregamento via fixture
    data_registro = models.DateTimeField()

    class Meta:
        db_table = 'consumo'
        verbose_name_plural = 'Consumo'