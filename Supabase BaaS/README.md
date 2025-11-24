# Lab-Supabase-BaaS

## Integrantes
- Isaac Villalobos Bonilla 2024124285
- Dilan Hernandez 2024063414
- Natalia Orozco Delgado 2024099161
- Carlos Abarca 2024138701

## Backend de Ventas con Supabase + FE Cliente en Python
Backend de ventas usando Supabase (PostgreSQL + PostgREST + Auth) que implementa:
- Modelo relacional con integridad referencial
- RLS (Row-Level Security) por país del cliente y por categoría del producto.
- Usuarios de prueba para validar el RLS.
- Una GUI en Python que se autentica y consume endpoints (listar, filtrar e insertar una factura con su detalle).

## Instalación

### Dependencias de Python
```bash
pip install supabase python-dotenv
```

### Configuración
1. Copiar `.env.template` a `.env`
2. Completar con tus credenciales de Supabase:
   ```
   SUPABASE_URL=tu_url_de_supabase
   SUPABASE_ANON_KEY=tu_clave_anonima
   USER_EMAIL=email_usuario@ejemplo.com
   USER_PASSWORD=contraseña_usuario
   ```

## Ejecución
```bash
python app/run_gui.py
```

## Instrucciones de Uso de la GUI

### Inicio de Sesión
1. Al abrir la aplicación, ir a la pestaña "Login"
2. Los campos Email y Password se pueden editar directamente
3. Por defecto cargan los valores del archivo .env, pero puedes cambiarlos
4. Hacer clic en "Iniciar Sesión" para conectar
5. Si la conexión es exitosa, te preguntará si quieres guardar las credenciales en .env

### Cambio de Usuario
- **Limpiar Campos**: Borra los campos de email y password
- **Guardar en .env**: Guarda las credenciales actuales en el archivo .env
- **Cerrar Sesión**: Cierra la sesión actual y permite cambiar de usuario sin reiniciar

### Gestión de Productos
1. Ir a la pestaña "Productos"
2. Ver lista de productos disponibles según tus permisos
3. Usar filtro por categoría para buscar productos específicos
4. Hacer clic en "Recargar" para actualizar la lista

### Gestión de Clientes
1. Ir a la pestaña "Clientes"
2. Ver lista de clientes disponibles según tus permisos de país
3. Usar filtro por país para buscar clientes específicos
4. Hacer clic en "Recargar" para actualizar la lista

### Crear Nueva Factura
1. Ir a la pestaña "Nueva Factura"
2. Seleccionar un cliente del combo desplegable
3. La fecha se establece automáticamente (se puede modificar)
4. **Para agregar productos:**
   - Seleccionar producto del combo (el precio se carga automáticamente)
   - Ingresar cantidad deseada
   - El total de línea se calcula en tiempo real
   - Hacer clic en "Agregar Línea"
5. Repetir paso 4 para todos los productos deseados
6. Ver el resumen en el panel derecho con el total de la factura
7. Hacer clic en "Crear Factura" para guardar

### Ver Facturas Existentes
1. Ir a la pestaña "Facturas"
2. Ver lista de todas las facturas según tus permisos
3. Filtrar por cliente específico si es necesario
4. Hacer clic en una factura para ver sus líneas de detalle en el panel inferior

### Administración
1. Ir a la pestaña "Administración"
2. Ver información del usuario conectado
3. **Actualizar Información**: Refresca los datos del usuario
4. **Verificar Permisos**: Muestra países y categorías autorizadas para tu usuario
5. Ver logs del sistema en tiempo real

## Características del Sistema de Permisos

### Row-Level Security (RLS)
- Cada usuario solo ve datos según sus permisos configurados
- Los permisos se basan en:
  - **País**: Solo clientes de países autorizados
  - **Categoría**: Solo productos de categorías autorizadas

### Usuarios de Ejemplo
Los usuarios deben existir en tu proyecto de Supabase y tener permisos configurados en las tablas:
- `user_allowed_country`: Define qué países puede ver cada usuario
- `user_allowed_category`: Define qué categorías de productos puede ver cada usuario

## Estructura del Proyecto
```
app/
  run_gui.py          # Script principal para ejecutar
  invoice_gui.py      # Interfaz gráfica principal
  main.py            # Funciones auxiliares
db/
  schema.sql         # Estructura de la base de datos
  trigger.sql        # Triggers para cálculos automáticos
  views.sql          # Vistas personalizadas
tests/
  permissions.sql    # Políticas de seguridad RLS
  postman.json       # Tests para API REST
```

## Notas Importantes
- La aplicación requiere conexión a internet y una cuenta de github para acceder a Supabase
- Los usuarios deben estar registrados en la sección Auth de tu proyecto Supabase
- Los permisos se gestionan a través de las tablas `user_allowed_country` y `user_allowed_category`

## Video explicativo
https://www.youtube.com/watch?v=fPlB8W3Ch0s
