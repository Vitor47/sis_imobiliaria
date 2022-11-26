from django.views.generic import DetailView, ListView
from .models import Imovel, Comodidades_Imovel
import django_filters


from django.shortcuts import render

def home(request):
    imoveis = Imovel.objects.filter(TIPO_VENDA="A_VENDA").order_by("-ID")
    return render(request, "sistema/imovel_list.html",{'imoveis': imoveis})
    

class ImovelDetailView(DetailView):
    model = Imovel
    template_name = 'sistema/imovel_detail.html'
    slug_field = 'SLUG'
    slug_url_kwarg = 'SLUG'