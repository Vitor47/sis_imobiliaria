from django.forms import ModelForm, ValidationError
from django.core.validators import RegexValidator
import re

def validate_cep(value):
    if not value.isdigit():
        raise ValidationError('O CEP deve conter apenas números')

def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('O CPF deve conter apenas números')

def validate_rg(value):
    if not value.isdigit():
        raise ValidationError('O RG deve conter apenas números')

def valida_limite(value):
    if value > 150.00:
        raise ValidationError('Você estrapolou o limite de gastos de um mês. O limite e 150')

validate_unique_number = RegexValidator(r'^[0,1,2,3,4,5,6,7,8,9]', 'O campo deve conter apenas numeros')
validate_unique_text = RegexValidator(r'^[a-zA-Z. '']', 'O campo deve conter apenas letras')
