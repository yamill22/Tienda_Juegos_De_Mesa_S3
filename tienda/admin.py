from django.contrib import admin
from tienda.models import Categoria, Juego, Pedido

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


class JuegoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'disponible', 'stock', 'formato_clp']
    list_filter = ['categoria', 'disponible']
    search_fields = ['nombre']

    def formato_clp(self, obj):
        return f"${obj.precio:,.0f}".replace(',', '.')
    formato_clp.short_description = 'Precio'

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'juego', 'nombre_cliente', 'cantidad', 'fecha_pedido']
    list_filter = ['juego']
    search_fields = ['nombre_cliente', 'correo']



admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Juego, JuegoAdmin)
admin.site.register (Pedido, PedidoAdmin)

