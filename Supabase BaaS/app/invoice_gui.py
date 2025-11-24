import tkinter as tk
from tkinter import ttk, messagebox
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import threading

class SupabaseInvoiceGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Facturación - Supabase")
        self.root.geometry("1200x800")
        
        # Variables de configuración
        load_dotenv()
        self.supabase_client = None
        self.user_info = None
        
        # Datos para los combos
        self.products_data = []
        self.customers_data = []
        self.categories_data = []
        self.countries_data = []
        
        # Variables para la creación de facturas
        self.invoice_lines = []
        self.current_product_price = 0.0  # Precio del producto seleccionado actualmente
        
        self.setup_ui()
        
    def setup_ui(self):
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de Login
        self.create_login_tab()
        
        # Pestaña de Productos
        self.create_products_tab()
        
        # Pestaña de Clientes
        self.create_customers_tab()
        
        # Pestaña de Facturas
        self.create_invoices_tab()
        
        # Pestaña de Nueva Factura
        self.create_new_invoice_tab()
        
        # Pestaña de Administración (si es necesario)
        self.create_admin_tab()
        
    def create_login_tab(self):
        login_frame = ttk.Frame(self.notebook)
        self.notebook.add(login_frame, text="🔐 Login")
        
        # Frame central para login
        center_frame = ttk.Frame(login_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(center_frame, text="Sistema de Facturación", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        # URL Supabase - OCULTO COMPLETAMENTE
        ttk.Label(center_frame, text="Supabase URL:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.url_label = ttk.Label(center_frame, text="●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●", 
                                foreground="gray", relief="sunken", padding=5, width=50)
        self.url_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Anon Key - OCULTO COMPLETAMENTE
        ttk.Label(center_frame, text="Anon Key:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.key_label = ttk.Label(center_frame, text="●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●", 
                                foreground="gray", relief="sunken", padding=5, width=50)
        self.key_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Email - MANTENER COMO ENTRY (EDITABLE)
        ttk.Label(center_frame, text="Email:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = ttk.Entry(center_frame, width=50)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)
        # Cargar email desde .env como valor por defecto, pero el usuario puede cambiarlo
        self.email_entry.insert(0, os.getenv("USER_EMAIL", ""))
        
        # Password - MANTENER COMO ENTRY (EDITABLE)
        ttk.Label(center_frame, text="Password:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(center_frame, width=50, show="*")
        self.password_entry.grid(row=4, column=1, padx=5, pady=5)
        # Cargar password desde .env como valor por defecto, pero el usuario puede cambiarlo
        self.password_entry.insert(0, os.getenv("USER_PASSWORD", ""))
        
        # Botón de login
        self.login_btn = ttk.Button(center_frame, text="🔑 Iniciar Sesión", command=self.login)
        self.login_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Botones adicionales para gestión de credenciales
        button_frame = ttk.Frame(center_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="🔄 Limpiar Campos", command=self.clear_credentials).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Guardar en .env", command=self.save_credentials_to_env).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🚪 Cerrar Sesión", command=self.logout).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = ttk.Label(center_frame, text="No conectado", foreground="red")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=5)
        
    def create_products_tab(self):
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text="📦 Productos")
        
        # Frame superior para filtros
        filter_frame = ttk.LabelFrame(products_frame, text="Filtros")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Categoría:").pack(side=tk.LEFT, padx=5)
        self.category_filter = ttk.Combobox(filter_frame, state="readonly", width=20)
        self.category_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="🔍 Filtrar", command=self.filter_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="🔄 Recargar", command=self.load_products).pack(side=tk.LEFT, padx=5)
        
        # Treeview para productos
        columns = ("ID", "Nombre", "Categoría", "Precio", "Fecha Creación")
        self.products_tree = ttk.Treeview(products_frame, columns=columns, show="headings")
        
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=150)
            
        self.products_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar para productos
        products_scrollbar = ttk.Scrollbar(products_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=products_scrollbar.set)
        products_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_customers_tab(self):
        customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(customers_frame, text="👥 Clientes")
        
        # Frame superior para filtros
        filter_frame = ttk.LabelFrame(customers_frame, text="Filtros")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="País:").pack(side=tk.LEFT, padx=5)
        self.country_filter = ttk.Combobox(filter_frame, state="readonly", width=20)
        self.country_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="🔍 Filtrar", command=self.filter_customers).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="🔄 Recargar", command=self.load_customers).pack(side=tk.LEFT, padx=5)
        
        # Treeview para clientes
        columns = ("ID", "Nombre", "Email", "País", "Fecha Creación")
        self.customers_tree = ttk.Treeview(customers_frame, columns=columns, show="headings")
        
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=150)
            
        self.customers_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar para clientes
        customers_scrollbar = ttk.Scrollbar(customers_frame, orient=tk.VERTICAL, command=self.customers_tree.yview)
        self.customers_tree.configure(yscrollcommand=customers_scrollbar.set)
        customers_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_invoices_tab(self):
        invoices_frame = ttk.Frame(self.notebook)
        self.notebook.add(invoices_frame, text="📄 Facturas")
        
        # Frame superior para filtros
        filter_frame = ttk.LabelFrame(invoices_frame, text="Filtros")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Cliente:").pack(side=tk.LEFT, padx=5)
        self.customer_filter = ttk.Combobox(filter_frame, state="readonly", width=30)
        self.customer_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="🔍 Filtrar", command=self.filter_invoices).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="🔄 Recargar", command=self.load_invoices).pack(side=tk.LEFT, padx=5)
        
        # Treeview para facturas
        columns = ("ID", "Cliente", "Fecha", "Total", "Fecha Creación")
        self.invoices_tree = ttk.Treeview(invoices_frame, columns=columns, show="headings")
        
        for col in columns:
            self.invoices_tree.heading(col, text=col)
            self.invoices_tree.column(col, width=150)
            
        self.invoices_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 0))
        
        # Frame para detalles de factura
        details_frame = ttk.LabelFrame(invoices_frame, text="Detalles de Factura")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview para líneas de factura
        line_columns = ("Producto", "Cantidad", "Precio Unit.", "Total Línea")
        self.invoice_lines_tree = ttk.Treeview(details_frame, columns=line_columns, show="headings", height=6)
        
        for col in line_columns:
            self.invoice_lines_tree.heading(col, text=col)
            self.invoice_lines_tree.column(col, width=120)
            
        self.invoice_lines_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Evento para mostrar detalles
        self.invoices_tree.bind("<<TreeviewSelect>>", self.show_invoice_details)
        
    def create_new_invoice_tab(self):
        new_invoice_frame = ttk.Frame(self.notebook)
        self.notebook.add(new_invoice_frame, text="➕ Nueva Factura")
        
        # Frame principal dividido en dos columnas
        main_frame = ttk.Frame(new_invoice_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Columna izquierda - Información de factura
        left_frame = ttk.LabelFrame(main_frame, text="Información de Factura")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Cliente
        ttk.Label(left_frame, text="Cliente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.invoice_customer = ttk.Combobox(left_frame, state="readonly", width=40)
        self.invoice_customer.grid(row=0, column=1, padx=5, pady=5)
        
        # Fecha
        ttk.Label(left_frame, text="Fecha:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.invoice_date = ttk.Entry(left_frame, width=40)
        self.invoice_date.grid(row=1, column=1, padx=5, pady=5)
        self.invoice_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Separador
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        
        # Agregar productos
        ttk.Label(left_frame, text="Producto:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.line_product = ttk.Combobox(left_frame, state="readonly", width=40)
        self.line_product.grid(row=3, column=1, padx=5, pady=5)
        self.line_product.bind("<<ComboboxSelected>>", self.on_product_selected)
        
        ttk.Label(left_frame, text="Cantidad:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.line_quantity = ttk.Entry(left_frame, width=40)
        self.line_quantity.grid(row=4, column=1, padx=5, pady=5)
        self.line_quantity.bind('<KeyRelease>', self.on_quantity_changed)
        self.line_quantity.bind('<Return>', self.on_quantity_enter)  # Enter para pasar al siguiente campo
        
        ttk.Label(left_frame, text="Precio Unitario:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.line_price_label = ttk.Label(left_frame, text="$0.00", font=("Arial", 10, "bold"), foreground="blue")
        self.line_price_label.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        
        # Mostrar total de línea en tiempo real
        ttk.Label(left_frame, text="Total Línea:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.line_total_label = ttk.Label(left_frame, text="$0.00", font=("Arial", 10, "bold"), foreground="blue")
        self.line_total_label.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="➕ Agregar Línea", command=self.add_invoice_line).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Quitar Línea", command=self.remove_invoice_line).pack(side=tk.LEFT, padx=5)
        
        # Columna derecha - Líneas de factura
        right_frame = ttk.LabelFrame(main_frame, text="Líneas de Factura")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Treeview para líneas temporales
        temp_columns = ("Producto", "Cantidad", "Precio", "Total")
        self.temp_lines_tree = ttk.Treeview(right_frame, columns=temp_columns, show="headings")
        
        for col in temp_columns:
            self.temp_lines_tree.heading(col, text=col)
            self.temp_lines_tree.column(col, width=100)
            
        self.temp_lines_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Total
        total_frame = ttk.Frame(right_frame)
        total_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(total_frame, text="Total Factura:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.total_label = ttk.Label(total_frame, text="$0.00", font=("Arial", 10, "bold"))
        self.total_label.pack(side=tk.RIGHT)
        
        # Botón crear factura
        ttk.Button(right_frame, text="💾 Crear Factura", command=self.create_invoice_with_lines).pack(pady=10)
        
    def create_admin_tab(self):
        admin_frame = ttk.Frame(self.notebook)
        self.notebook.add(admin_frame, text="⚙️ Administración")
        
        # Frame principal
        main_admin_frame = ttk.Frame(admin_frame)
        main_admin_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Información del usuario
        user_info_frame = ttk.LabelFrame(main_admin_frame, text="Información del Usuario")
        user_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.user_info_text = tk.Text(user_info_frame, height=8, state=tk.DISABLED, wrap=tk.WORD)
        self.user_info_text.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones de administración
        buttons_frame = ttk.LabelFrame(main_admin_frame, text="Acciones Administrativas")
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_row1 = ttk.Frame(buttons_frame)
        button_row1.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_row1, text="🔄 Actualizar Información", command=self.update_user_info).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_row1, text="🔍 Verificar Permisos", command=self.verify_permissions).pack(side=tk.LEFT, padx=(0, 5))
        
        # Área de logs
        logs_frame = ttk.LabelFrame(main_admin_frame, text="Logs del Sistema")
        logs_frame.pack(fill=tk.BOTH, expand=True)
        
        self.logs_text = tk.Text(logs_frame, height=10, state=tk.DISABLED, wrap=tk.WORD)
        logs_scrollbar = ttk.Scrollbar(logs_frame, command=self.logs_text.yview)
        self.logs_text.configure(yscrollcommand=logs_scrollbar.set)
        
        self.logs_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        logs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
    def log_message(self, message):
        """Agregar mensaje a los logs"""
        try:
            self.logs_text.config(state=tk.NORMAL)
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.logs_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.logs_text.see(tk.END)
            self.logs_text.config(state=tk.DISABLED)
        except:
            pass  # Si no existe el widget, ignorar
            
    def update_user_info(self):
        """Actualizar información del usuario en la pestaña admin"""
        if not self.user_info:
            return
            
        try:
            info_text = f"""
Usuario: {self.user_info.email}
ID: {self.user_info.id}
Última conexión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Estado: ✅ Conectado y autenticado
"""
            
            if hasattr(self, 'user_info_text'):
                self.user_info_text.config(state=tk.NORMAL)
                self.user_info_text.delete(1.0, tk.END)
                self.user_info_text.insert(1.0, info_text)
                self.user_info_text.config(state=tk.DISABLED)
                
        except Exception as e:
            self.log_message(f"Error actualizando información: {e}")
            
    def verify_permissions(self):
        """Verificar permisos detallados del usuario"""
        if not self.supabase_client or not self.user_info:
            messagebox.showwarning("Advertencia", "No hay sesión activa")
            return
            
        try:
            # Verificar permisos de país
            user_countries = self.supabase_client.table("user_allowed_country").select("*, countries(name)").eq("user_id", self.user_info.id).execute()
            
            # Verificar permisos de categoría  
            user_categories = self.supabase_client.table("user_allowed_category").select("*, categories(name)").eq("user_id", self.user_info.id).execute()
            
            countries_info = []
            if user_countries.data:
                for uc in user_countries.data:
                    country_name = uc.get('countries', {}).get('name', 'N/A') if uc.get('countries') else 'N/A'
                    countries_info.append(f"- {country_name} ({uc['country_code']})")
            
            categories_info = []
            if user_categories.data:
                for uc in user_categories.data:
                    category_name = uc.get('categories', {}).get('name', 'N/A') if uc.get('categories') else 'N/A'
                    categories_info.append(f"- {category_name}")
                    
            permissions_detail = f"""
🌍 PAÍSES AUTORIZADOS ({len(user_countries.data if user_countries.data else [])}):
{chr(10).join(countries_info) if countries_info else '  No hay países autorizados'}

📦 CATEGORÍAS AUTORIZADAS ({len(user_categories.data if user_categories.data else [])}):
{chr(10).join(categories_info) if categories_info else '  No hay categorías autorizadas'}

⚠️ IMPORTANTE:
- Solo puedes ver datos de países y categorías autorizadas
- Los permisos son gestionados por Row Level Security (RLS)
- Contacta al administrador para cambios de permisos
"""
            
            messagebox.showinfo("Permisos del Usuario", permissions_detail)
            self.log_message("Permisos verificados correctamente")
            
        except Exception as e:
            error_msg = f"Error verificando permisos: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.log_message(error_msg)
            
    def show_statistics(self):
        """Mostrar estadísticas del usuario"""
        if not self.supabase_client:
            messagebox.showwarning("Advertencia", "No hay conexión a la base de datos")
            return
            
        try:
            # Contar productos disponibles
            products_count = len(self.products_data)
            
            # Contar clientes disponibles
            customers_count = len(self.customers_data)
            
            # Contar facturas
            invoices = self.supabase_client.table("invoices").execute()
            invoices_count = len(invoices.data) if invoices.data else 0
            
            # Calcular total facturado
            total_amount = sum(inv.get('total_amount', 0) for inv in (invoices.data or []))
            
            stats = f"""
📊 ESTADÍSTICAS DEL USUARIO

📦 Productos disponibles: {products_count}
👥 Clientes disponibles: {customers_count}  
📄 Facturas totales: {invoices_count}
💰 Total facturado: ${total_amount:.2f}

📈 Esta información se basa en los datos
   que tu usuario tiene autorizado a ver
   según las políticas RLS configuradas.
"""
            
            messagebox.showinfo("Estadísticas", stats)
            self.log_message(f"Estadísticas mostradas: {products_count} productos, {customers_count} clientes, {invoices_count} facturas")
            
        except Exception as e:
            error_msg = f"Error calculando estadísticas: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.log_message(error_msg)
            
    def on_product_selected(self, event):
        """Se ejecuta cuando se selecciona un producto en el combobox"""
        try:
            product_selected = self.line_product.get()
            if not product_selected:
                return
                
            # Encontrar el producto seleccionado y obtener su precio
            product_name = product_selected.split(" - $")[0]
            for product in self.products_data:
                if product["name"] == product_name:
                    # Establecer el precio del producto en el label (solo lectura)
                    self.line_price_label.config(text=f"${product['unit_price']:.2f}")
                    
                    # Guardar el precio para usar en cálculos
                    self.current_product_price = float(product["unit_price"])
                    
                    # Limpiar la cantidad para que el usuario la ingrese
                    self.line_quantity.delete(0, tk.END)
                    self.line_quantity.insert(0, "1")  # Cantidad por defecto
                    
                    # Dar foco al campo de cantidad
                    self.line_quantity.focus_set()
                    self.line_quantity.select_range(0, tk.END)  # Seleccionar todo el texto
                    
                    # Calcular total inicial
                    self.calculate_line_total()
                    
                    self.log_message(f"Producto seleccionado: {product['name']} - Precio: ${product['unit_price']}")
                    break
                    
        except Exception as e:
            # Log del error pero no mostrar al usuario para no interrumpir el flujo
            self.log_message(f"Error estableciendo precio automático: {str(e)}")
            
    def on_quantity_changed(self, event):
        """Se ejecuta cuando cambia la cantidad"""
        self.calculate_line_total()
        
    def on_quantity_enter(self, event):
        """Se ejecuta cuando se presiona Enter en cantidad"""
        # Como ya no hay campo de precio editable, agregar línea directamente
        self.add_invoice_line()
        
    def calculate_line_total(self):
        """Calcula y muestra el total de la línea actual"""
        try:
            quantity_str = self.line_quantity.get().strip()
            
            if quantity_str and hasattr(self, 'current_product_price'):
                quantity = float(quantity_str)
                price = self.current_product_price
                
                if quantity > 0 and price >= 0:
                    line_total = quantity * price
                    self.line_total_label.config(text=f"${line_total:.2f}", foreground="green")
                else:
                    self.line_total_label.config(text="$0.00", foreground="red")
            else:
                self.line_total_label.config(text="$0.00", foreground="gray")
                
        except ValueError:
            self.line_total_label.config(text="Error", foreground="red")
        except Exception:
            self.line_total_label.config(text="$0.00", foreground="gray")
        

    def login(self):
        try:
            # Obtener valores DIRECTAMENTE del archivo .env (NO de la GUI)
            url = os.getenv("SUPABASE_URL", "").strip()
            key = os.getenv("SUPABASE_ANON_KEY", "").strip()
            
            # Obtener email y password de la GUI
            email = self.email_entry.get().strip()
            password = self.password_entry.get().strip()
            
            # Validar que todos los valores estén presentes
            if not url:
                messagebox.showerror("Error", "SUPABASE_URL no está configurado en el archivo .env")
                self.log_message("Error: SUPABASE_URL no configurado")
                return
                
            if not key:
                messagebox.showerror("Error", "SUPABASE_ANON_KEY no está configurado en el archivo .env")
                self.log_message("Error: SUPABASE_ANON_KEY no configurado")
                return
                
            if not email:
                messagebox.showerror("Error", "El email es requerido")
                return
                
            if not password:
                messagebox.showerror("Error", "El password es requerido")
                return
                
            self.status_label.config(text="Conectando...", foreground="orange")
            self.root.update()
            
            # Log de intento de conexión (SIN mostrar credenciales)
            self.log_message("Intentando conectar a Supabase...")
            
            # Crear cliente Supabase
            self.supabase_client = create_client(url, key)
            
            # Autenticar
            auth = self.supabase_client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if not auth.session:
                raise Exception("Error en la autenticación")
                
            self.user_info = auth.user
            self.status_label.config(text=f"Conectado como: {auth.user.email}", foreground="green")
            
            # Cargar datos iniciales
            self.load_initial_data()
            
            # Actualizar información en admin tab
            self.update_user_info()
            self.log_message("Conexión establecida exitosamente")
            
            # Preguntar si quiere guardar las credenciales en .env (opcional)
            if messagebox.askyesno("Guardar Credenciales", 
                                   "¿Desea guardar estas credenciales en el archivo .env para futuras sesiones?"):
                self.save_credentials_to_env()
            
            messagebox.showinfo("Éxito", "Conexión exitosa!")
            
        except Exception as e:
            self.status_label.config(text="Error de conexión", foreground="red")
            error_msg = f"Error de conexión: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)

            
    def load_initial_data(self):
        if not self.supabase_client:
            return
            
        try:
            # Cargar categorías
            categories = self.supabase_client.table("categories").select("*").execute()
            self.categories_data = categories.data if categories.data else []
            category_names = ["Todas"] + [cat["name"] for cat in self.categories_data]
            self.category_filter["values"] = category_names
            self.category_filter.set("Todas")
            
            # Cargar países
            countries = self.supabase_client.table("countries").select("*").execute()
            self.countries_data = countries.data if countries.data else []
            country_names = ["Todos"] + [f"{country['name']} ({country['code']})" for country in self.countries_data]
            self.country_filter["values"] = country_names
            self.country_filter.set("Todos")
            
            # Cargar datos principales
            self.load_products()
            self.load_customers()
            self.load_invoices()
            
            # Mostrar información sobre permisos
            self.show_user_permissions()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos: {str(e)}")
            
    def show_user_permissions(self):
        """Muestra información sobre los permisos del usuario"""
        if not self.supabase_client or not self.user_info:
            return
            
        try:
            # Verificar permisos de país
            user_countries = self.supabase_client.table("user_allowed_country").select("*, countries(name)").eq("user_id", self.user_info.id).execute()
            countries_allowed = [f"{uc['countries']['name']} ({uc['country_code']})" for uc in user_countries.data if uc.get('countries')] if user_countries.data else []
            
            # Verificar permisos de categoría
            user_categories = self.supabase_client.table("user_allowed_category").select("*, categories(name)").eq("user_id", self.user_info.id).execute()
            categories_allowed = [uc['categories']['name'] for uc in user_categories.data if uc.get('categories')] if user_categories.data else []
            
            # Construir mensaje informativo
            permissions_info = f"""
Usuario: {self.user_info.email}

Países autorizados: {', '.join(countries_allowed) if countries_allowed else 'Ninguno'}

Categorías autorizadas: {', '.join(categories_allowed) if categories_allowed else 'Ninguna'}

📝 Nota: Solo podrás ver y gestionar datos según estos permisos.
"""
            
            # Actualizar el status label con info básica
            basic_info = f"Conectado: {self.user_info.email} | Países: {len(countries_allowed)} | Categorías: {len(categories_allowed)}"
            self.status_label.config(text=basic_info, foreground="green")
            
            # Si no tiene permisos, mostrar advertencia
            if not countries_allowed or not categories_allowed:
                messagebox.showwarning("Permisos Limitados", 
                    f"⚠️ Advertencia: Tu usuario tiene permisos limitados.\n\n"
                    f"Países autorizados: {len(countries_allowed)}\n"
                    f"Categorías autorizadas: {len(categories_allowed)}\n\n"
                    f"Contacta al administrador si necesitas más permisos.")
                    
        except Exception as e:
            print(f"Error verificando permisos: {str(e)}")  # Log error but don't show to user
            
    def load_products(self):
        if not self.supabase_client:
            return
            
        try:
            # Consulta con join a categorías
            products = self.supabase_client.table("products").select("*, categories(name)").execute()
            self.products_data = products.data
            
            # Limpiar treeview
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
                
            # Llenar treeview
            for product in products.data:
                category_name = product.get("categories", {}).get("name", "N/A") if product.get("categories") else "N/A"
                self.products_tree.insert("", tk.END, values=(
                    product["id"],
                    product["name"],
                    category_name,
                    f"${product['unit_price']:.2f}",
                    product.get("created_at", "")[:10] if product.get("created_at") else ""
                ))
                
            # Actualizar combo para nueva factura
            if products.data:
                product_options = [f"{p['name']} - ${p['unit_price']:.2f}" for p in products.data]
                self.line_product["values"] = product_options
                
                # Limpiar selección anterior si existe
                if hasattr(self, 'line_product') and self.line_product.get():
                    # Si hay un producto seleccionado que ya no existe, limpiarlo
                    current_selection = self.line_product.get()
                    if current_selection not in product_options:
                        self.line_product.set("")
                        if hasattr(self, 'line_price_label'):
                            self.line_price_label.config(text="$0.00")
                        if hasattr(self, 'current_product_price'):
                            delattr(self, 'current_product_price')
                        self.line_quantity.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando productos: {str(e)}")
            
    def load_customers(self):
        if not self.supabase_client:
            return
            
        try:
            # Consulta con join a países
            customers = self.supabase_client.table("customers").select("*, countries(name)").execute()
            self.customers_data = customers.data
            
            # Limpiar treeview
            for item in self.customers_tree.get_children():
                self.customers_tree.delete(item)
                
            # Llenar treeview
            for customer in customers.data:
                country_name = customer.get("countries", {}).get("name", "N/A") if customer.get("countries") else "N/A"
                self.customers_tree.insert("", tk.END, values=(
                    customer["id"],
                    customer["name"],
                    customer.get("email", ""),
                    f"{country_name} ({customer['country_code']})",
                    customer.get("created_at", "")[:10] if customer.get("created_at") else ""
                ))
                
            # Actualizar combos
            customer_options = [f"{c['name']} ({c.get('email', 'Sin email')})" for c in customers.data]
            self.customer_filter["values"] = ["Todos"] + customer_options
            self.customer_filter.set("Todos")
            self.invoice_customer["values"] = customer_options
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando clientes: {str(e)}")
            
    def load_invoices(self):
        if not self.supabase_client:
            return
            
        try:
            # Consulta con join a clientes
            invoices = self.supabase_client.table("invoices").select("*, customers(name)").execute()
            
            # Limpiar treeview
            for item in self.invoices_tree.get_children():
                self.invoices_tree.delete(item)
                
            # Llenar treeview
            for invoice in invoices.data:
                customer_name = invoice.get("customers", {}).get("name", "N/A") if invoice.get("customers") else "N/A"
                self.invoices_tree.insert("", tk.END, values=(
                    invoice["id"],
                    customer_name,
                    invoice.get("invoice_date", ""),
                    f"${invoice.get('total_amount', 0):.2f}",
                    invoice.get("created_at", "")[:10] if invoice.get("created_at") else ""
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando facturas: {str(e)}")
            
    def filter_products(self):
        if not self.supabase_client:
            return
            
        try:
            category_selected = self.category_filter.get()
            
            if category_selected == "Todas":
                self.load_products()
            else:
                # Encontrar el ID de la categoría
                category_id = None
                for cat in self.categories_data:
                    if cat["name"] == category_selected:
                        category_id = cat["id"]
                        break
                        
                if category_id:
                    products = self.supabase_client.table("products").select("*, categories(name)").eq("category_id", category_id).execute()
                    
                    # Limpiar y llenar treeview
                    for item in self.products_tree.get_children():
                        self.products_tree.delete(item)
                        
                    for product in products.data:
                        category_name = product.get("categories", {}).get("name", "N/A") if product.get("categories") else "N/A"
                        self.products_tree.insert("", tk.END, values=(
                            product["id"],
                            product["name"],
                            category_name,
                            f"${product['unit_price']:.2f}",
                            product.get("created_at", "")[:10] if product.get("created_at") else ""
                        ))
                        
        except Exception as e:
            messagebox.showerror("Error", f"Error filtrando productos: {str(e)}")
            
    def filter_customers(self):
        if not self.supabase_client:
            return
            
        try:
            country_selected = self.country_filter.get()
            
            if country_selected == "Todos":
                self.load_customers()
            else:
                # Extraer código del país del formato "Nombre (CODE)"
                country_code = country_selected.split("(")[-1].rstrip(")")
                
                customers = self.supabase_client.table("customers").select("*, countries(name)").eq("country_code", country_code).execute()
                
                # Limpiar y llenar treeview
                for item in self.customers_tree.get_children():
                    self.customers_tree.delete(item)
                    
                for customer in customers.data:
                    country_name = customer.get("countries", {}).get("name", "N/A") if customer.get("countries") else "N/A"
                    self.customers_tree.insert("", tk.END, values=(
                        customer["id"],
                        customer["name"],
                        customer.get("email", ""),
                        f"{country_name} ({customer['country_code']})",
                        customer.get("created_at", "")[:10] if customer.get("created_at") else ""
                    ))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error filtrando clientes: {str(e)}")
            
    def filter_invoices(self):
        if not self.supabase_client:
            return
            
        try:
            customer_selected = self.customer_filter.get()
            
            if customer_selected == "Todos":
                self.load_invoices()
            else:
                # Encontrar el ID del cliente
                customer_name = customer_selected.split(" (")[0]
                customer_id = None
                for customer in self.customers_data:
                    if customer["name"] == customer_name:
                        customer_id = customer["id"]
                        break
                        
                if customer_id:
                    invoices = self.supabase_client.table("invoices").select("*, customers(name)").eq("customer_id", customer_id).execute()
                    
                    # Limpiar y llenar treeview
                    for item in self.invoices_tree.get_children():
                        self.invoices_tree.delete(item)
                        
                    for invoice in invoices.data:
                        customer_name = invoice.get("customers", {}).get("name", "N/A") if invoice.get("customers") else "N/A"
                        self.invoices_tree.insert("", tk.END, values=(
                            invoice["id"],
                            customer_name,
                            invoice.get("invoice_date", ""),
                            f"${invoice.get('total_amount', 0):.2f}",
                            invoice.get("created_at", "")[:10] if invoice.get("created_at") else ""
                        ))
                        
        except Exception as e:
            messagebox.showerror("Error", f"Error filtrando facturas: {str(e)}")
            
    def show_invoice_details(self, event):
        if not self.supabase_client:
            return
            
        selection = self.invoices_tree.selection()
        if not selection:
            return
            
        try:
            # Obtener ID de la factura seleccionada
            item = self.invoices_tree.item(selection[0])
            invoice_id = item["values"][0]
            
            # Cargar líneas de la factura
            lines = self.supabase_client.table("invoice_lines").select("*, products(name)").eq("invoice_id", invoice_id).execute()
            
            # Limpiar y llenar treeview de detalles
            for item in self.invoice_lines_tree.get_children():
                self.invoice_lines_tree.delete(item)
                
            for line in lines.data:
                product_name = line.get("products", {}).get("name", "N/A") if line.get("products") else "N/A"
                self.invoice_lines_tree.insert("", tk.END, values=(
                    product_name,
                    f"{line['quantity']:.2f}",
                    f"${line['unit_price']:.2f}",
                    f"${line['line_total']:.2f}"
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando detalles: {str(e)}")
            
    def add_invoice_line(self):
        try:
            product_selected = self.line_product.get()
            quantity_str = self.line_quantity.get().strip()
            
            if not product_selected:
                messagebox.showerror("Error", "Seleccione un producto")
                return
                
            if not quantity_str:
                messagebox.showerror("Error", "Ingrese la cantidad")
                return
                
            if not hasattr(self, 'current_product_price'):
                messagebox.showerror("Error", "Precio del producto no disponible")
                return
                
            quantity = float(quantity_str)
            price = self.current_product_price
            
            if quantity <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
                
            # Encontrar el producto seleccionado
            product_name = product_selected.split(" - $")[0]
            product = None
            for p in self.products_data:
                if p["name"] == product_name:
                    product = p
                    break
                    
            if not product:
                messagebox.showerror("Error", "Producto no encontrado")
                return
                
            # Calcular total de línea
            line_total = quantity * price
            
            # Agregar a la lista temporal
            line_data = {
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": quantity,
                "unit_price": price,
                "line_total": line_total
            }
            
            self.invoice_lines.append(line_data)
            
            # Agregar al treeview temporal
            self.temp_lines_tree.insert("", tk.END, values=(
                product["name"],
                f"{quantity:.2f}",
                f"${price:.2f}",
                f"${line_total:.2f}"
            ))
            
            # Actualizar total
            self.update_invoice_total()
            
            # Limpiar cantidad pero mantener el producto seleccionado y precio
            self.line_quantity.delete(0, tk.END)
            self.line_quantity.insert(0, "1")  # Cantidad por defecto
            
            # Dar foco al campo de cantidad para seguir agregando
            self.line_quantity.focus_set()
            self.line_quantity.select_range(0, tk.END)
            
            self.log_message(f"Línea agregada: {product['name']} x{quantity:.2f} = ${line_total:.2f}")
            
        except ValueError as e:
            if "float" in str(e).lower():
                messagebox.showerror("Error", "La cantidad debe ser un número válido")
            else:
                messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error agregando línea: {str(e)}")
            self.log_message(f"Error agregando línea: {str(e)}")
            
    def remove_invoice_line(self):
        selection = self.temp_lines_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una línea para eliminar")
            return
            
        # Obtener índice de la línea seleccionada
        item = self.temp_lines_tree.item(selection[0])
        index = self.temp_lines_tree.index(selection[0])
        
        # Eliminar de la lista
        del self.invoice_lines[index]
        
        # Eliminar del treeview
        self.temp_lines_tree.delete(selection[0])
        
        # Actualizar total
        self.update_invoice_total()
        
    def update_invoice_total(self):
        total = sum(line["line_total"] for line in self.invoice_lines)
        self.total_label.config(text=f"${total:.2f}")
        
    def create_invoice_with_lines(self):
        if not self.supabase_client:
            messagebox.showerror("Error", "No está conectado")
            return
            
        try:
            customer_selected = self.invoice_customer.get()
            invoice_date = self.invoice_date.get()
            
            if not customer_selected:
                messagebox.showerror("Error", "Seleccione un cliente")
                return
                
            if not self.invoice_lines:
                messagebox.showerror("Error", "Agregue al menos una línea a la factura")
                return
                
            # Encontrar el ID del cliente
            customer_name = customer_selected.split(" (")[0]
            customer_id = None
            for customer in self.customers_data:
                if customer["name"] == customer_name:
                    customer_id = customer["id"]
                    break
                    
            if not customer_id:
                messagebox.showerror("Error", "Cliente no encontrado")
                return
                
            # Calcular total
            total_amount = sum(line["line_total"] for line in self.invoice_lines)
            
            # Crear factura
            invoice_data = {
                "customer_id": customer_id,
                "invoice_date": invoice_date,
                "total_amount": total_amount
            }
            
            invoice = self.supabase_client.table("invoices").insert(invoice_data).execute()
            
            if not invoice.data:
                raise Exception("Error creando la factura")
                
            invoice_id = invoice.data[0]["id"]
            
            # Crear líneas de factura
            for line in self.invoice_lines:
                line_data = {
                    "invoice_id": invoice_id,
                    "product_id": line["product_id"],
                    "quantity": line["quantity"],
                    "unit_price": line["unit_price"],
                    "line_total": line["line_total"]
                }
                
                self.supabase_client.table("invoice_lines").insert(line_data).execute()
                
            # Limpiar formulario
            self.invoice_lines.clear()
            for item in self.temp_lines_tree.get_children():
                self.temp_lines_tree.delete(item)
            self.update_invoice_total()
            self.invoice_customer.set("")
            self.invoice_date.delete(0, tk.END)
            self.invoice_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
            
            # Recargar facturas
            self.load_invoices()
            self.log_message(f"Factura #{invoice_id} creada exitosamente con {len(self.invoice_lines)} líneas")
            
            messagebox.showinfo("Éxito", f"Factura #{invoice_id} creada exitosamente!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creando factura: {str(e)}")
            
    def clear_credentials(self):
        """Limpiar los campos de email y password"""
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.log_message("Campos de credenciales limpiados")
        
    def save_credentials_to_env(self):
        """Guardar las credenciales actuales en el archivo .env"""
        try:
            email = self.email_entry.get().strip()
            password = self.password_entry.get().strip()
            
            if not email or not password:
                messagebox.showwarning("Advertencia", "Por favor complete ambos campos antes de guardar")
                return
            
            # Leer el archivo .env actual
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
            
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Actualizar las líneas correspondientes
                updated_lines = []
                email_updated = False
                password_updated = False
                
                for line in lines:
                    if line.startswith('USER_EMAIL='):
                        updated_lines.append(f'USER_EMAIL={email}\n')
                        email_updated = True
                    elif line.startswith('USER_PASSWORD='):
                        updated_lines.append(f'USER_PASSWORD={password}\n')
                        password_updated = True
                    else:
                        updated_lines.append(line)
                
                # Si no existían las líneas, agregarlas al final
                if not email_updated:
                    updated_lines.append(f'USER_EMAIL={email}\n')
                if not password_updated:
                    updated_lines.append(f'USER_PASSWORD={password}\n')
                
                # Escribir el archivo actualizado
                with open(env_path, 'w', encoding='utf-8') as f:
                    f.writelines(updated_lines)
                
                self.log_message("Credenciales guardadas en archivo .env")
                messagebox.showinfo("Éxito", "Credenciales guardadas exitosamente en el archivo .env")
                
            else:
                messagebox.showerror("Error", "No se encontró el archivo .env")
                
        except Exception as e:
            error_msg = f"Error guardando credenciales: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def logout(self):
        """Cerrar la sesión actual y permitir cambiar de usuario"""
        try:
            if self.supabase_client and self.user_info:
                # Cerrar sesión en Supabase
                self.supabase_client.auth.sign_out()
                self.log_message(f"Sesión cerrada para: {self.user_info.email}")
            
            # Limpiar variables de sesión
            self.supabase_client = None
            self.user_info = None
            
            # Limpiar datos
            self.products_data = []
            self.customers_data = []
            self.categories_data = []
            self.countries_data = []
            self.invoice_lines = []
            
            # Limpiar todas las tablas/treeviews
            for tree in [self.products_tree, self.customers_tree, self.invoices_tree, 
                        self.invoice_lines_tree, self.temp_lines_tree]:
                for item in tree.get_children():
                    tree.delete(item)
            
            # Limpiar combos
            for combo in [self.category_filter, self.country_filter, self.customer_filter,
                         self.invoice_customer, self.line_product]:
                combo['values'] = []
                combo.set("")
            
            # Actualizar estado
            self.status_label.config(text="Sesión cerrada - Puede iniciar con otro usuario", foreground="orange")
            self.log_message("Sesión cerrada exitosamente")
            
            messagebox.showinfo("Sesión Cerrada", "Sesión cerrada exitosamente. Puede iniciar sesión con otro usuario.")
            
        except Exception as e:
            error_msg = f"Error cerrando sesión: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SupabaseInvoiceGUI()
    app.run()
