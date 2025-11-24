import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configuración desde variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")

# DEBUG: Ver qué valores se están cargando
print("🔍 Valores cargados:")
print(f"URL: {SUPABASE_URL}")
print(f"KEY: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "KEY: None")
print(f"EMAIL: {USER_EMAIL}")

def login() -> Client:
    # Verificar que las variables existan
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: Variables de entorno no encontradas")
        print("   Asegúrate de tener un archivo .env con:")
        print("   SUPABASE_URL=tu_url")
        print("   SUPABASE_ANON_KEY=tu_key")
        raise SystemExit(1)
    
    sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    auth = sb.auth.sign_in_with_password({
        "email": USER_EMAIL, 
        "password": USER_PASSWORD
    })
    
    if not auth.session:
        raise SystemExit("Error de login.")
        
    print("Conectado como:", auth.user.email)
    return sb

def list_my_products(sb: Client):
    res = sb.table("products").select("*").execute()
    print("Productos (RLS aplicado):", res.data)

def list_my_customers(sb: Client):
    res = sb.table("customers").select("*").execute()
    print("Clientes (RLS aplicado):", res.data)

def create_invoice(sb: Client, customer_id: int):
    inv = sb.table("invoices").insert({"customer_id": customer_id}).select("*").execute()
    print("Factura:", inv.data)
    return inv.data[0]["id"]

def add_line(sb: Client, invoice_id: int, product_id: int, qty: float, unit_price: float):
    line_total = round(qty * unit_price, 2)
    line = {
        "invoice_id": invoice_id,
        "product_id": product_id,
        "quantity": qty,
        "unit_price": unit_price,
        "line_total": line_total
    }
    res = sb.table("invoice_lines").insert(line).select("*").execute()
    print("Línea:", res.data)

def show_invoice_with_lines(sb: Client, invoice_id: int):
    inv = sb.table("invoices").select("*").eq("id", invoice_id).execute()
    lines = sb.table("invoice_lines").select("*").eq("invoice_id", invoice_id).execute()
    print("Factura:", inv.data)
    print("Líneas:", lines.data)

if __name__ == "__main__":
    sb = login()
    list_my_products(sb)
    list_my_customers(sb)
    # Completar: input() para IDs y crear factura + líneas