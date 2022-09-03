from django.contrib import admin
from  django.contrib.auth.models  import  Group
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from django.forms import ModelForm, ValidationError
from .models import Endereco, Imovel, Detalhes_Imovel, Comodidades_Imovel, Inquilino, Imovel_Detalhes_Imovel, GastosInquilino, ContaBancariaImovel

admin.site.unregister(Group)
admin.site.site_header = 'Admin Imobiliária Miolo'
admin.site.index_title  =  "Administração da Imobiliária"

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ("RUA", "NUMERO", "CEP", "BAIRRO", "CIDADE", "CREATED", "EDIT")
    list_filter = ("CREATED", "EDIT")
    list_per_page = 8

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html("<img src='{}'  width='100' height='80' />".format(obj.IMAGEM_PRINCIPAL.url))
    image_tag.short_description = 'Imagem'
    list_display = ("NOME_IMOVEL", "image_tag", "DATA_IMOVEL", "CREATED", "EDIT")
    list_filter = ("CREATED", "EDIT", "TIPO_VENDA")
    search_fields = ("NOME_IMOVEL",)
    fields = ("NOME_IMOVEL", "SLUG", "DATA_IMOVEL", "TIPO_VENDA", "VALOR_IMOVEL", "IMAGEM_PRINCIPAL", "DESCRICAO", "ENDERECO", "NUMERO_QUARTOS", "NUMERO_BANHEIROS", "GARAGEM", "USERCAD")
    prepopulated_fields = {"SLUG" : ("NOME_IMOVEL",)}
    list_per_page = 8
    
    
@admin.register(Detalhes_Imovel)
class DetalhesImovel(admin.ModelAdmin):
    list_display = ("SITUACAO", "TIPO", "TIPO_CONDOMINIO", "CREATED", "EDIT")
    list_filter = ("CREATED", "EDIT")
    list_per_page = 8

@admin.register(Comodidades_Imovel)
class ComodidadesImovel(admin.ModelAdmin):
    list_display = ("imovel_pertencente", "VALOR", "CREATED", "EDIT")
    list_filter = ("CREATED", "EDIT")
    list_per_page = 8

#class ImovelInline(admin.TabularInline):
   #model = Imovel

@admin.register(Inquilino)
class InquilinoImovel(admin.ModelAdmin):
    list_display = ("NOME", "imovel_pertencente", "EMAIL", "telefone_formatado", "cpf_formatado", "CREATED", "EDIT")
    list_filter = ("CREATED", "EDIT")
    search_fields = ("NOME", )
    list_per_page = 8
    #inlines = [ImovelInline]

@admin.register(GastosInquilino)
class InquilinoGastos(admin.ModelAdmin):
    list_display = ("INQUILINO", "LUZ", "AGUA", "INTERNET", "TELEFONE", "CREATED", "EDIT")
    list_filter = ("CREATED", "EDIT")
    list_per_page = 8

    
@admin.register(Imovel_Detalhes_Imovel)
class List_Detalhes(admin.ModelAdmin):
    list_display = ("ID_IMOVEL", "ID_DETALHES_IMOVEL")
    list_per_page = 8

@admin.register(ContaBancariaImovel)
class Conta_Bancaria_Imovel(admin.ModelAdmin):
    list_display = ("VALOR", "IPTU", "IMOVEL", "CONDOMINIO", "GARAGEM", "CREATED", "EDIT")
    list_filter = ("CREATED", "EDIT")
    list_per_page = 8
