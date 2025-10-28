# Sistema de Gestión de Biblioteca

Sistema Django para la gestión integral de una biblioteca con funcionalidades de préstamos, socios, multas y administración.

## Estructura del Proyecto

```
biblioteca/
├── biblioteca/          # Configuración global
├── socios/             # Gestión de socios
├── libros/             # Administración de libros y préstamos
├── multas/             # Gestión de penalizaciones
├── usuarios/           # Autenticación y personal
├── templates/          # Plantillas HTML con Bootstrap 5.3
├── static/             # Archivos estáticos
└── requirements.txt    # Dependencias
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Base de datos SQLite configurada automáticamente

3. Ejecutar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Crear superusuario:
```bash
python manage.py createsuperuser
```

5. Ejecutar servidor:
```bash
python manage.py runserver
```

## Acceso al Sistema

**Usuario administrador creado:**
- Usuario: `admin`
- Contraseña: `admin123`
- Email: `admin@biblioteca.com`

## Características

- **Gestión de Socios**: Alta, baja, modificación
- **Administración de Libros**: Catálogo, préstamos, devoluciones
- **Sistema de Multas**: Penalizaciones automáticas por retrasos
- **Autenticación**: Sistema de usuarios con roles
- **Interfaz Responsive**: Bootstrap 5.3

## Buenas Prácticas Implementadas

- Nomenclatura CamelCase para clases, snake_case para métodos
- Principios SRP y DRY
- Manejo de excepciones con try/except
- Validaciones en modelos
- Formateo homogéneo del código