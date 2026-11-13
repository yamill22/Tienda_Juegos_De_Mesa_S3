from django.shortcuts import render
from tienda.models import Categoria, Juego

def catalogo(request):
    juegos = Juego.objects.filter(disponible=True).select_related('categoria').order_by('nombre')
    nombre = request.GET.get('nombre', '').strip()
    categoria_id = request.GET.get('categoria', '')

    if nombre:
        juegos = juegos.filter(nombre__icontains=nombre)

    if categoria_id.isdecimal():
        juegos = juegos.filter(categoria_id=int(categoria_id))

    categorias = Categoria.objects.order_by('nombre')
    return render(request, 'catalogo.html', {
        'juegos': juegos,
        'categorias': categorias,
        'nombre': nombre,
        'categoria_seleccionada': categoria_id if categoria_id.isdecimal() else '',
    })
    
