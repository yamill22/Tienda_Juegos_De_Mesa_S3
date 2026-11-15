from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from tienda.models import Categoria, Juego, Pedido
from tienda.forms import FormVenta

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
    if request.method == 'POST':
        with transaction.atomic():
            juego = get_object_or_404(
                Juego.objects.select_related('categoria'),
                pk=juego_id,
                disponible=True,
            )
            form = FormVenta(request.POST, juego=juego)

            if form.is_valid():
                cantidad = form.cleaned_data['cantidad']

                stock_actualizado = Juego.objects.filter(
                    pk=juego.pk,
                    disponible=True,
                    stock__gte=cantidad,
                ).update(stock=F('stock') - cantidad)

                if stock_actualizado:
                    pedido = Pedido.objects.create(
                        juego=juego,
                        nombre_cliente=form.cleaned_data['nombre_cliente'],
                        correo=form.cleaned_data['correo'],
                        telefono=form.cleaned_data['telefono'],
                        cantidad=cantidad,
                    )
                    return redirect('comprobante', codigo=pedido.codigo)

                juego.refresh_from_db(fields=['stock'])
                form.add_error(
                    'cantidad',
                    f'Solo hay {juego.stock} unidades disponibles.',
                )
    else:
        juego = get_object_or_404(
            Juego.objects.select_related('categoria'),
            pk=juego_id,
            disponible=True,
        )
        form = FormVenta(juego=juego)

    return render(request, 'detalle.html', {
        'juego': juego,
        'form': form,
    })


def comprobante_pedido(request, codigo):
    pedido = get_object_or_404(
        Pedido.objects.select_related('juego'),
        codigo=codigo,
    )
    return render(request, 'comprobante.html', {'pedido': pedido})
