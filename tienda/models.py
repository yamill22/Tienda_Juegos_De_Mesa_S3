from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random

class Categoria(models.Model):

    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='juegos/', null=True, blank=True, verbose_name="Imagen de la caja")
    precio = models.PositiveIntegerField()
    jugadores = models.CharField(max_length=50, verbose_name="Cantidad de jugadores")
    edad_minima = models.PositiveIntegerField(verbose_name="Edad minima recomendada")
    stock = models.PositiveIntegerField(verbose_name="Unidades en bodega")
    disponible = models.BooleanField(default=True, verbose_name="Disponible para la venta")

    def __str__(self):
        return self.nombre

    @property
    def precio_chileno(self):
        return f"${self.precio:,.0f}".replace(',', '.')



def generar_codigo_pedido():
    return str(random.randint(100000000000, 9999999999999))

class Pedido(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    cantidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    
    codigo = models.CharField(max_length=20, default=generar_codigo_pedido, editable=False, unique=True)

    def __str__(self):
        return f"Pedido {self.codigo} - {self.nombre_cliente}"
    