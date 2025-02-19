from django.db import models

class Usuario(models.Model):
    ROL_CHOICES = [
        ('oferente', 'Oferente'),
        ('buscador', 'Buscador'),
        ('ambos', 'Ambos'),
    ]
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)

class Servicio(models.Model):
    CATEGORIA_CHOICES = [
        ('tecnologia', 'Tecnología'),
        ('gastronomia', 'Gastronomía'),
        ('mantenimiento', 'Mantenimiento'),
        ('salud', 'Salud'),
        ('maestranza', 'Maestranza'),
        ('ocio', 'Ocio'),
        ('gerontologia', 'Gerontología'),
        ('venta', 'Venta'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    duracion_estimada = models.CharField(max_length=50)
    disponibilidad_horaria = models.CharField(max_length=100)
    id_oferente = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    id_busqueda = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)

class Calificacion(models.Model):
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    id_busqueda = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField()
