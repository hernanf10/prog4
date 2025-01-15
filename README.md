#directorio de trabajo
	/scrum
#Dockerfile para generar django-container
# Usar una imagen base de Python
FROM python:3.9
# Establecer el directorio de trabajo
WORKDIR /app
# Copiar los archivos de requisitos
COPY requirements.txt .
# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt
# Copiar el resto de la aplicación
COPY . .
# Exponer el puerto que usará la aplicación
EXPOSE 8000
# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "proyectos.wsgi:application", "--bind", "0.0.0.0:8000"]

#requirements.txt 
Django>=3.2,<4.0
djangorestframework
mysqlclient
drf-yasg
gunicorn

#generar imagen docker
docker build -t django-container .

#correr docker mysql-container se monta el volumen mysql en la raiz del proyecto para mantener la persistencia
docker run --rm -d --name mysql-container --network deploy1 -e TZ=America/Argentina/Buenos_Aires -e MYSQL_ROOT_PASSWORD=hernanf10 -e MYSQL_DATABASE=app -e MYSQL_USER=user -e MYSQL_PASSWORD=hernanf10 -v "$PWD"/mysql:/var/lib/mysql mysql:8.0-debian --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

#crear proyecto - se ejecuta la primera vez
docker run --rm --name django-container --network deploy1 --link mysql-container:mysql -p 8000:8000 -it -v "$PWD":/app django-container django-admin startproject proyectos
#crear app - se ejecuta la primera vez
docker run --rm --name django-container --network deploy1 --link mysql-container:mysql -p 8000:8000 -it -v "$PWD"/proyectos:/app django-container python manage.py startapp servicios
#correr docker django-container
docker run --rm --name django-container --network deploy1 --link mysql-container:mysql -p 8000:8000 -d -v "$PWD"/proyectos:/app django-container

#correr docker adminer
docker run --rm -it -d --name adminer --network deploy1 -p 9000:8080 adminer:latest

#correr docker nginx 
docker run --rm --name nginx-container --network deploy1 -d -p 80:80 -v "$PWD/nginx.conf:/etc/nginx/conf.d/default.conf" -v "$PWD/proyectos/staticfiles:/app/staticfiles" nginx

#archivo nginx.conf en la raiz del proyecto
server {
    listen 80;
    server_name 192.168.100.251;  # dominio o IP

    location /static/ {
        alias /app/staticfiles/;  # Ruta donde se encuentran los archivos estáticos
    }

    location / {
        proxy_pass http://django-container:8000;  # Nombre del contenedor de Django
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

#generar el siguiente modelo de datos
1. Diagrama Entidad-Relación (DER)
Usuarios
---------
- id (PK)
- nombre
- email
- contraseña
- rol (oferente, buscador, ambos)

Servicios
---------
- id (PK)
- titulo
- descripcion
- categoria (tecnologia, gastronomia, mantenimiento, salud, maestranza, ocio, gerontologia, venta)
- duracion_estimada
- disponibilidad_horaria
- id_oferente (FK -> Usuarios.id)

Solicitudes
-----------
- id (PK)
- id_servicio (FK -> Servicios.id)
- id_busqueda (FK -> Usuarios.id)
- comentario
- estado (pendiente, aceptada, rechazada)

Calificaciones
--------------
- id (PK)
- id_servicio (FK -> Servicios.id)
- id_busqueda (FK -> Usuarios.id)
- calificacion (1-5)
- comentario

#conectar mysqlclient
con datos de la base mysql

en setting.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app',
        'USER': 'user',
        'PASSWORD': 'hernanf10',
        'HOST': 'mysql-container',
        'PORT': '3306',
    }
}

#migraciones
docker exec -it django-container python manage.py makemigrations
docker exec -it django-container python manage.py migrate


#INSTALLED_APPS settings.py
 servicios
 djangorestframework
 drf-yasg
 
#generar api para crud de las entidades
#generar doc swager/openapi
#habilitar admin django para la aplicacion
en admin.py
