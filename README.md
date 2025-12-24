# Backend Django - Guía de Configuración

## 📋 Requisitos Previos

- Python 3.10+
- PostgreSQL (o Neon Database)
- pip (gestor de paquetes de Python)

## 🚀 Instalación Inicial

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Backend
```

### 2. Crear y activar el entorno virtual

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> ⚠️ Si tienes problemas con la ejecución de scripts en PowerShell, ejecuta primero:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install django djangorestframework psycopg2-binary python-dotenv
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_db?sslmode=require
```

> 💡 Si usas Neon Database, copia la URL de conexión directamente desde el dashboard de Neon.

---

## 🗃️ Migraciones de Base de Datos

### Paso 1: Verificar el estado de las migraciones

Este comando muestra todas las migraciones y su estado (aplicadas o pendientes):

```bash
python manage.py showmigrations
```

**Salida esperada:**
- `[X]` = Migración aplicada
- `[ ]` = Migración pendiente

### Paso 2: Crear nuevas migraciones

Cuando modifiques modelos en `models.py`, ejecuta:

```bash
python manage.py makemigrations
```

Para una app específica:
```bash
python manage.py makemigrations auth_app
```

### Paso 3: Ver el SQL que se ejecutará (opcional)

Antes de aplicar, puedes ver el SQL que generará la migración:

```bash
python manage.py sqlmigrate auth_app 0001_initial
```

### Paso 4: Aplicar las migraciones

Aplica todas las migraciones pendientes:

```bash
python manage.py migrate
```

Para una app específica:
```bash
python manage.py migrate auth_app
```

### Paso 5: Verificar que se aplicaron correctamente

```bash
python manage.py showmigrations
```

Todas las migraciones deberían mostrar `[X]`.

---

## 🔄 Flujo Completo de Migraciones

### Resumen de comandos en orden:

```bash
# 1. Activar entorno virtual
venv\Scripts\activate          # Windows CMD
# o
.\venv\Scripts\Activate.ps1    # Windows PowerShell

# 2. Verificar estado actual
python manage.py showmigrations

# 3. Crear migraciones (si hay cambios en models.py)
python manage.py makemigrations

# 4. Aplicar migraciones
python manage.py migrate

# 5. Verificar que se aplicaron
python manage.py showmigrations
```

---

## 🛠️ Comandos Útiles

### Crear un superusuario (admin)
```bash
python manage.py createsuperuser
```

### Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

### Acceder al shell de Django
```bash
python manage.py shell
```

### Revertir una migración específica
```bash
python manage.py migrate auth_app 0001_initial
```

### Eliminar todas las migraciones y empezar de cero
> ⚠️ **PELIGRO**: Esto eliminará todos los datos

```bash
# 1. Eliminar archivos de migración (excepto __init__.py)
# 2. Eliminar la tabla django_migrations en la DB
# 3. Ejecutar makemigrations y migrate nuevamente
```

---

## 📁 Estructura del Proyecto

```
Backend/
├── config/
│   ├── settings.py      # Configuración principal
│   ├── urls.py          # URLs principales
│   └── wsgi.py
├── auth_app/
│   ├── migrations/      # Archivos de migración
│   ├── models.py        # Modelos de datos
│   ├── views.py         # Vistas/controladores
│   ├── urls.py          # URLs de la app
│   └── admin.py
├── .env                 # Variables de entorno (NO subir a git)
├── manage.py
└── README.md
```

---

## 📊 Modelo User

El modelo `User` en `auth_app/models.py` tiene la siguiente estructura:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigAutoField | Clave primaria (auto-generada) |
| `name` | CharField(100) | Nombre del usuario |
| `email` | EmailField | Email único |
| `password` | CharField(100) | Contraseña |
| `direction` | CharField(100) | Dirección |
| `phone_number` | CharField(100) | Teléfono |
| `isVendor` | BooleanField | Si es vendedor (default: False) |

**Tabla en la base de datos:** `users`

---

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "relation does not exist"
Las migraciones no se han aplicado. Ejecuta:
```bash
python manage.py migrate
```

### Error: "FATAL: password authentication failed"
Verifica que la `DATABASE_URL` en `.env` sea correcta.

### Error de ejecución de scripts en PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 Notas Adicionales

- Siempre activa el entorno virtual antes de ejecutar comandos de Django
- Nunca subas el archivo `.env` al repositorio (ya está en `.gitignore`)
- Haz `makemigrations` después de cualquier cambio en `models.py`
- Revisa las migraciones antes de aplicarlas en producción
