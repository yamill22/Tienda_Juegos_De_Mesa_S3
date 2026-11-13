from django.shortcuts import get_object_or_404, render
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
    

def detalle_juego(request, juego_id):
    juego = get_object_or_404(
        Juego.objects.select_related('categoria'),
        pk=juego_id,
        disponible=True,
    )

    return render(request, 'detalle.html', {'juego': juego})
