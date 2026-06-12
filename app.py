import os
from flask import Flask
import psycopg2

app = Flask(__name__)

# Configuración por Variables de Entorno (Requerimiento de la guía)
APP_NAME = os.getenv("APP_NAME", "Solucion DevOps Flask")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "inventario")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")

def obtener_conexion():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def inicio():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        estado_conexion = f"✔ Conectado exitosamente a PostgreSQL ({db_version})"
        color = "green"
    except Exception as e:
        estado_conexion = f"❌ Error de conexión: {str(e)}"
        color = "red"

    return f"""
    <h1>Nombre de la aplicación: {APP_NAME}</h1>
    <h2>Versión actual: {APP_VERSION}</h2>
    <p style="color: {color}; font-weight: bold;">Estado de conexión: {estado_conexion}</p>
    <br>
    <a href="/productos" style="font-size: 18px; font-weight: bold;">🛒 Ir a visualizar todos los productos almacenados</a>
    """

@app.route("/productos")
def listar_productos():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos;")
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()

        tabla_html = "".join([
            f"<tr><td>{p[0]}</td><td>{p[1]}</td><td>${p[2]}</td><td>{p[3]}</td></tr>" 
            for p in productos
        ])
        
        if not tabla_html:
            tabla_html = "<tr><td colspan='4'>No hay productos registrados aún. ¡Créalos en pgAdmin!</td></tr>"
    except Exception as e:
        tabla_html = f"<tr><td colspan='4' style='color:red;'>Error al cargar tabla o no existe: {str(e)}</td></tr>"

    return f"""
    <h2>Ruta: Visualización de Productos</h2>
    <table border="1" cellpadding="8" style="border-collapse: collapse;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th>ID</th><th>Nombre</th><th>Precio</th><th>Stock</th>
            </tr>
        </thead>
        <tbody>
            {tabla_html}
        </tbody>
    </table>
    <br>
    <a href="/">⬅ Volver al Inicio</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)