from django.db import models


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


