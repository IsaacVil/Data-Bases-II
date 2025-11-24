#!/usr/bin/env python3
"""
Script para ejecutar la aplicación GUI de Facturación con Supabase
"""

import sys
import os

# Agregar el directorio de la app al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from invoice_gui import SupabaseInvoiceGUI

if __name__ == "__main__":
    print("🚀 Iniciando Sistema de Facturación - Supabase GUI")
    print("=" * 50)
    
    try:
        app = SupabaseInvoiceGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")
        sys.exit(1)