# 📡 API Endpoints - Tienda Online

Base URL: `http://localhost:8000`

---

## 🔐 Autenticación (`/api/auth/`)

### 1. Registrar Cliente
```
POST /api/auth/register_client
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "email": "cliente@ejemplo.com",
    "password": "password123",
    "name": "Juan Pérez"
}
```

**Respuesta exitosa (201):**
```json
{
    "message": "Client registered successfully"
}
```

---

### 2. Registrar Vendedor
```
POST /api/auth/register_vendor
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "email": "vendedor@ejemplo.com",
    "password": "password123",
    "name": "María López",
    "direction": "Av. Principal 123",
    "phone_number": "0991234567"
}
```

**Respuesta exitosa (201):**
```json
{
    "message": "Vendor registered successfully"
}
```

---

### 3. Ver Perfil de Vendedor
```
GET /api/auth/vendors/{vendor_id}/
```

**Headers:**
```
Content-Type: application/json
```

**Parámetros URL:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| vendor_id | int | ID del vendedor |

**Respuesta exitosa (200):**
```json
{
    "id": 1,
    "name": "María López",
    "email": "vendedor@ejemplo.com",
    "direction": "Av. Principal 123",
    "phone_number": "0991234567",
    "average_rating": null,
    "reviews": []
}
```

---

## 🛍️ Productos (`/api/products/`)

### 4. Obtener Todas las Etiquetas
```
GET /api/products/tags/
```

**Headers:**
```
Content-Type: application/json
```

**Respuesta exitosa (200):**
```json
{
    "count": 8,
    "tags": [
        {"value": "gaming", "label": "Gaming"},
        {"value": "laptop", "label": "Laptop"},
        {"value": "pc", "label": "PC"},
        {"value": "celular", "label": "Celular"},
        {"value": "tablet", "label": "Tablet"},
        {"value": "accesorio", "label": "Accesorio"},
        {"value": "ssd", "label": "SSD"},
        {"value": "ram", "label": "RAM"}
    ]
}
```

---

### 5. Obtener Productos por Etiqueta
```
GET /api/products/by-tag/{tag_name}/
```

**Headers:**
```
Content-Type: application/json
```

**Parámetros URL:**
| Parámetro | Tipo | Valores válidos |
|-----------|------|-----------------|
| tag_name | string | gaming, laptop, pc, celular, tablet, accesorio, ssd, ram |

**Respuesta exitosa (200):**
```json
{
    "tag": "gaming",
    "count": 2,
    "products": [
        {
            "id": 1,
            "id_product": "PROD-001",
            "name_product": "Laptop Gaming",
            "description": "Laptop de alta gama",
            "price": "1500.00",
            "stock": 10,
            "vendor_name": "María López",
            "tags": ["gaming", "laptop"]
        }
    ]
}
```

---

### 6. Agregar Producto
```
POST /api/products/add/
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "id_product": "PROD-001",
    "name_product": "Laptop Gaming ASUS ROG",
    "description": "Laptop para gaming de alta gama con RTX 4060",
    "price": 1500.00,
    "stock": 10,
    "vendor_id": 1,
    "tags": ["gaming", "laptop"]
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| id_product | string | ✅ | Código único del producto |
| name_product | string | ✅ | Nombre del producto |
| description | string | ✅ | Descripción detallada |
| price | decimal | ✅ | Precio (máx 10 dígitos, 2 decimales) |
| stock | integer | ✅ | Cantidad disponible |
| vendor_id | integer | ✅ | ID del vendedor (debe ser is_vendor=true) |
| tags | array | ❌ | Lista de etiquetas válidas |

**Respuesta exitosa (201):**
```json
{
    "message": "Producto creado exitosamente",
    "product": {
        "id": 1,
        "id_product": "PROD-001",
        "name_product": "Laptop Gaming ASUS ROG",
        "price": "1500.00",
        "stock": 10,
        "vendor": "María López",
        "tags": ["gaming", "laptop"]
    }
}
```

---

### 7. Ver Estado de Producto
```
GET /api/products/{product_id}/status/
```

**Headers:**
```
Content-Type: application/json
Authorization: Token <token>
```

**Respuesta exitosa (200):**
```json
{
    "status": "ACTIVO"
}
```

---

### 8. Actualizar Estado de Producto
```
PATCH /api/products/{product_id}/status/
```

**Headers:**
```
Content-Type: application/json
Authorization: Token <token>
```

**Body:**
```json
{
    "status": "PAUSADO"
}
```

| Campo | Tipo | Valores válidos |
|-------|------|-----------------|
| status | string | ACTIVO, PAUSADO, VENDIDO |

**Respuesta exitosa (200):**
```json
{
    "message": "Estado de la publicación actualizado correctamente",
    "product_id": 1,
    "new_status": "PAUSADO"
}
```

---

## 🛒 Carrito de Compras (`/api/ventas/`)

### 9. Crear/Obtener Carrito
```
POST /api/ventas/cart/
```

**Headers:**
```
Content-Type: application/json
Authorization: Token <token>
```

**Respuesta exitosa (200):**
```json
{
    "items": [
        {
            "product": "Laptop Gaming",
            "quantity": 2,
            "price": 1500.00,
            "subtotal": 3000.00
        }
    ]
}
```

---

### 10. Agregar Producto al Carrito
```
POST /api/ventas/cart/add/
```

**Headers:**
```
Content-Type: application/json
Authorization: Token <token>
```

**Body:**
```json
{
    "product_id": 1,
    "quantity": 2
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| product_id | integer | ✅ | ID del producto |
| quantity | integer | ❌ | Cantidad (default: 1) |

**Respuesta exitosa (201):**
```json
{
    "message": "Product added to cart",
    "cart_item": {
        "product": "Laptop Gaming",
        "quantity": 2,
        "price": "1500.00"
    }
}
```

---

### 11. Obtener Total del Carrito
```
GET /api/ventas/cart/total/
```

**Headers:**
```
Content-Type: application/json
Authorization: Token <token>
```

**Respuesta exitosa (200):**
```json
{
    "total": 3000.00
}
```

---

## 🔧 Administración

### 12. Panel de Administración Django
```
GET /admin/
```

Acceso al panel de administración de Django (requiere superusuario).

---

## 📋 Resumen de Endpoints

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| POST | /api/auth/register_client | ❌ | Registrar cliente |
| POST | /api/auth/register_vendor | ❌ | Registrar vendedor |
| GET | /api/auth/vendors/{id}/ | ❌ | Ver perfil vendedor |
| GET | /api/products/tags/ | ❌ | Listar etiquetas |
| GET | /api/products/by-tag/{tag}/ | ❌ | Productos por etiqueta |
| POST | /api/products/add/ | ❌ | Agregar producto |
| GET | /api/products/{id}/status/ | ✅ | Ver estado producto |
| PATCH | /api/products/{id}/status/ | ✅ | Actualizar estado |
| POST | /api/ventas/cart/ | ✅ | Crear/ver carrito |
| POST | /api/ventas/cart/add/ | ✅ | Agregar al carrito |
| GET | /api/ventas/cart/total/ | ✅ | Total del carrito |

---

## 🏷️ Etiquetas Válidas

- `gaming` - Gaming
- `laptop` - Laptop
- `pc` - PC
- `celular` - Celular
- `tablet` - Tablet
- `accesorio` - Accesorio
- `ssd` - SSD
- `ram` - RAM

---

## 📌 Estados de Producto

- `ACTIVO` - Producto disponible para compra
- `PAUSADO` - Producto pausado temporalmente
- `VENDIDO` - Producto vendido/agotado
