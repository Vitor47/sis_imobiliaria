from django.urls import path
from .import views
app_name = "sistema"

urlpatterns = [
    path("", views.ImovelListView.as_view(), name="List"),
    #path("", views.filter_app, name='filter_app')
    path("<slug:SLUG>/", views.ImovelDetailView.as_view(), name="detail")
]