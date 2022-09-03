from django.views.generic import DetailView, ListView
from .models import Imovel, Comodidades_Imovel
import django_filters


from django.shortcuts import render

# Create your views here.
'''
def filter_app(request):
    TIPO_VENDA = ["A_VENDA", "N_VENDA"]
    imovel = ["A_VENDA"]
    return render(request, 'sistema/imovel_list.html', {'TIPO_VENDA': TIPO_VENDA, 'imovel':imovel})
'''

class ImovelListView(ListView):
    model = Imovel
    template_name = 'sistema/imovel_list.html'
    paginate_by = 6
    

class ImovelDetailView(DetailView):
    model = Imovel
    template_name = 'sistema/imovel_detail.html'
    slug_field = 'SLUG'
    slug_url_kwarg = 'SLUG'