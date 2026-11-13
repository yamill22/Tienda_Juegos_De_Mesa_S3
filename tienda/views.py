from django.shortcuts import render
from tienda.models import Juego

def catalogo(request):
    juegos = Juego.objects.filter(disponible=True).select_related('categoria').order_by('nombre')
    return render(request, 'catalogo.html', {'juegos': juegos})
    
