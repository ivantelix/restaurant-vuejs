# Restaurant Order System

Sistema de pedidos para restaurante con interfaz drag-and-drop para la selección de ingredientes.

## Estructura del Proyecto

```
restaurant/
├── backend/               # Django backend
│   ├── apps/             # Aplicaciones modulares
│   ├── core/             # Configuración central
│   └── manage.py
└── frontend/             # Vue.js frontend
    ├── src/
    └── public/
```

## Backend Setup

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar migraciones:
```bash
cd backend
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

## Frontend Setup

1. Instalar dependencias:
```bash
cd frontend
npm install
```

2. Ejecutar servidor de desarrollo:
```bash
npm run serve
```

## Características

### Backend
- Autenticación y autorización con JWT
- Gestión de usuarios y roles
- Gestión de productos e ingredientes
- API REST para órdenes y productos
- Dashboard administrativo

### Frontend
- Interfaz drag-and-drop para selección de ingredientes
- Diseño responsive con AdminLTE 3
- Gestión de estado con Vuex
- Rutas protegidas
- Sidebar con navegación 