from django.db import models
from django.forms import ModelForm, ValidationError
from django import forms
from django.contrib.auth.models import User
from .validators import validate_cep, validate_cpf, validate_rg, validate_unique_text, validate_unique_number, valida_limite
from django.core.validators import RegexValidator
from django.urls import reverse
from django.db.models import F

class Endereco(models.Model):
    OPC_ESTADO = (
        ("RS", "Rio Grande do Sul"),
    )
    RUA = models.CharField('Rua:', max_length=200, null=False, blank=False, validators=[validate_unique_text])
    NUMERO = models.IntegerField('Numero da casa:', null=False, blank=False, validators=[validate_unique_number])
    COMPLEMENTO = models.CharField('Complemento', max_length=200, null=False, blank=False, validators=[validate_unique_text])
    CEP = models.CharField('Cep:', max_length=8, null=False, blank=False, validators=[validate_cep])
    BAIRRO = models.CharField('Bairro:', max_length=50, null=False, blank=False, validators=[validate_unique_text])
    CIDADE = models.CharField('Cidade:', max_length=50, null=False, blank=False, validators=[validate_unique_text])
    ESTADO = models.CharField('Estado:',max_length=2, choices=OPC_ESTADO, blank=False, null=False, validators=[validate_unique_text])
    USERCAD = models.ForeignKey(User, on_delete=models.CASCADE)
    CREATED = models.DateTimeField('Adicionou:', auto_now_add=True)
    EDIT = models.DateTimeField('Editou:', auto_now=True)
 
    class Meta:
            db_table = "ENDERECOS"
            verbose_name_plural  =  "Endereços"

    def __str__(self):
        return self.RUA

class Detalhes_Imovel(models.Model):
    TIPO_SITUACAO = (
        ("NOVO", "Imóvel novo"),
        ("USADO", "Imóvel usado")
    )
    TIPO_IMOVEL = (
        ("RES", "Casa Residencial"),
        ("APE", "Apartamento")
    )
    TIPO_CONDOMINIO = (
        ("FECHADO", "Condominio Fechado"),
        ("ABERTO", "Condominio Aberto")
    )
    
    ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    NOME = models.CharField('Nome do detalhe', max_length=200, null=False, blank=False, validators=[validate_unique_text])
    SITUACAO = models.CharField('Situação:',max_length=5, choices=TIPO_SITUACAO, blank=False, null=False)
    TIPO = models.CharField('Tipo Imóvel:',max_length=3, choices=TIPO_IMOVEL, blank=False, null=False)
    TIPO_CONDOMINIO = models.CharField('Tipo do Condominio:',max_length=7, choices=TIPO_CONDOMINIO, blank=False, null=False)
    AREA_UTIL = models.IntegerField('Metros quadrados da área util:', null=False, blank=False, validators=[validate_unique_number])
    AREA_TOTAL = models.IntegerField('Metros quadrados da área total:', null=False, blank=False, validators=[validate_unique_number])
    USERCAD = models.ForeignKey(User, on_delete=models.CASCADE)
    CREATED = models.DateTimeField('Adicionou:', auto_now_add=True)
    EDIT = models.DateTimeField('Editou:', auto_now=True)
 
    class Meta:
            db_table = "IMOVEL_DETALHES"
            verbose_name_plural  =  "Detalhes dos Imóveis"

    def __str__(self):
        return self.SITUACAO

class Imovel(models.Model):
    TIPO_VENDA = (
        ("A_VENDA", "A venda"),
        ("N_VENDA", "Não está a venda")
    )
    ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    SLUG = models.SlugField('Slug:', max_length=255, unique=True, validators=[validate_unique_text])
    NOME_IMOVEL = models.CharField('Nome do imóvel:', max_length=255, validators=[validate_unique_text])
    DATA_IMOVEL = models.DateField('Data do imóvel:', null=False, blank=False)
    VALOR_IMOVEL = models.DecimalField('Valor do Imovel:', max_digits = 12, decimal_places = 2, null=False, blank=False, validators=[validate_unique_number])
    TIPO_VENDA = models.CharField('Situação:',max_length=7, choices=TIPO_VENDA, blank=False, null=False)
    IMAGEM_PRINCIPAL = models.ImageField()
    DESCRICAO = models.TextField('Descrição:',)
    ENDERECO = models.OneToOneField(Endereco, on_delete=models.SET_NULL, null=True)
    NUMERO_QUARTOS = models.IntegerField('Numero de quartos:', null=False, blank=False, validators=[validate_unique_number])
    NUMERO_BANHEIROS = models.IntegerField('Numero de banheiros:', null=False, blank=False, validators=[validate_unique_number])
    GARAGEM = models.IntegerField('Quantidade de espaço na garagem:', null=False, blank=False, validators=[validate_unique_number])
    CREATED = models.DateTimeField('Adicionou:', auto_now_add=True)
    EDIT = models.DateTimeField('Editou:', auto_now=True)
    USERCAD = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.NOME_IMOVEL

    def get_absolute_url(self):
        return reverse("imovel:detail", kwargs={"SLUG": self.SLUG})

    class Meta:
        db_table = "IMOVEIS"
        verbose_name_plural  =  "Lista de Imóveis"
        ordering = ("-CREATED",)

class Imovel_Detalhes_Imovel(models.Model):
    ID_IMOVEL = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    ID_DETALHES_IMOVEL = models.ForeignKey(Detalhes_Imovel, on_delete=models.CASCADE)

    class Meta:
        db_table = "IMOVEL_DETALHES_IMOVEL"
        verbose_name_plural  =  "Detalhes dos Imoveis com o Imovel"

class Comodidades_Imovel(models.Model):
    IMOVEL_PERTENCENTE = models.ManyToManyField(Imovel)
    VALOR = models.CharField('Digite a comodidade do imovel:', max_length=255, validators=[validate_unique_text])
    CREATED = models.DateTimeField('Adicionou:', auto_now_add=True)
    EDIT = models.DateTimeField('Editou:', auto_now=True)

    def imovel_pertencente(self):
        return ",".join([str(c) for c in self.IMOVEL_PERTENCENTE.all()])

    def __unicode__(self):
        return "{0}".format(self.NOME)

    class Meta:
        db_table = "IMOVEIS_COMODIDADES"
        verbose_name_plural  =  "comodidades dos imóveis"

class Inquilino(models.Model):
    OPC_SEXO = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")
    )
    NOME = models.CharField('Nome:', max_length=100, validators=[validate_unique_text])
    EMAIL = models.EmailField('Email:', null=False, blank=False)
    TELEFONE = models.CharField('Telefone:', max_length=12, validators=[validate_unique_number])
    CPF = models.CharField('CPF:', max_length=11, validators=[validate_cpf])
    RG = models.CharField('RG:', max_length=10, validators=[validate_rg])
    DATA_NASCIMENTO = models.DateField('Data Nascimento:', null=False, blank=False)
    PROFISSAO = models.CharField('Profissão:', max_length=50, null=False, blank=False, validators=[validate_unique_text])
    SEXO = models.CharField('Sexo:',max_length=1, choices=OPC_SEXO, blank=False, null=False)
    ENDERECO = models.OneToOneField(Endereco, on_delete=models.SET_NULL, null=True)
    IMOVEL = models.ManyToManyField(Imovel)
    USERCAD = models.ForeignKey(User, on_delete=models.CASCADE)
    CREATED = models.DateTimeField('Adicionou:',auto_now_add=True)
    EDIT = models.DateTimeField('Editou:',auto_now=True)

    def cpf_formatado(self):
        return f'{self.CPF[0:3]}.{self.CPF[3:6]}.{self.CPF[6:9]}-{self.CPF[9:11]}'
    cpf_formatado.short_description = 'CPF'

    def telefone_formatado(self):
        return f'({self.TELEFONE[0:2]}){self.TELEFONE[2:7]}-{self.TELEFONE[7:11]}'
    telefone_formatado.short_description = 'TELEFONE'

    def imovel_pertencente(self):
        return ",".join([str(i) for i in self.IMOVEL.all()])

    def __unicode__(self):
        return "{0}".format(self.NOME)

    def __str__(self):
        return self.NOME

    class Meta:
        db_table = "INQUILINOS"
        verbose_name_plural  =  "Lista de Inquilinos"

class GastosInquilino(models.Model):
    LUZ = models.DecimalField("Conta de Luz:", max_digits = 8, decimal_places = 2 , null=False, blank=False, validators=[valida_limite])
    AGUA = models.DecimalField("Conta de Água:", max_digits = 8, decimal_places = 2, null=False, blank=False, validators=[valida_limite])
    INTERNET = models.DecimalField("Conta de Internet:", max_digits = 8, decimal_places = 2, null=False, blank=False, validators=[validate_unique_number])
    TELEFONE = models.DecimalField("Conta de Telefone:", max_digits = 8, decimal_places = 2, null=False, blank=False, validators=[validate_unique_number])
    MERCADO = models.DecimalField("Gastos com Mercado:", max_digits = 8, decimal_places = 2, null=False, blank=False, validators=[validate_unique_number])
    GASTOS_EXTRAS = models.DecimalField("Gastos Extras:", max_digits = 8, decimal_places = 2, null=False, blank=False, validators=[validate_unique_number])
    INQUILINO = models.OneToOneField(Inquilino, on_delete=models.SET_NULL, null=True)
    USERCAD = models.ForeignKey(User, on_delete=models.CASCADE)
    CREATED = models.DateTimeField('Adicionou:',auto_now_add=True)
    EDIT = models.DateTimeField('Editou:',auto_now=True)

    class Meta:
        db_table = "GASTOS_INQULINO"
        verbose_name_plural  =  "Lista de Gastos dos Inquilinos"
        ordering = ("-CREATED",)

class ContaBancariaImovel(models.Model):
    VALOR = models.DecimalField("Conta Bancaria:", max_digits = 8, decimal_places = 2, null=False, blank=False)
    IPTU = models.DecimalField("Gastos com Iptu:", max_digits = 8, decimal_places = 2, null=False, blank=False, validators=[validate_unique_number])
    CONDOMINIO = models.DecimalField("Gastos com Condominio:", max_digits = 8, decimal_places = 2, null=False, blank=False, validators=[validate_unique_number])
    GARAGEM = models.DecimalField("Gastos com Garagem:", max_digits = 8, decimal_places = 2, null=False, blank=False, validators=[validate_unique_number])
    IMOVEL = models.OneToOneField(Imovel, on_delete=models.SET_NULL, null=True)
    USERCAD = models.ForeignKey(User, on_delete=models.CASCADE)
    CREATED = models.DateTimeField('Adicionou:',auto_now_add=True)
    EDIT = models.DateTimeField('Editou:',auto_now=True)

    def save(self, *args, **kwargs):
        self.VALOR = ((self.VALOR) - (self.IPTU) - (self.CONDOMINIO) - (self.GARAGEM))
        super(ContaBancariaImovel, self).save(*args, **kwargs)

    class Meta:
        db_table = "CONTA_BANCARIA_IMOVEL"
        verbose_name_plural  =  "Conta Bancaria do Imovel"
        ordering = ("-CREATED",)