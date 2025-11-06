from flask import Flask, request, jsonify
import psycopg2
from dotenv import load_dotenv

import os
# ==========================================
# 🧠 Cargar variables de entorno
# ==========================================
load_dotenv()

app = Flask(__name__)

# ==========================================
#  Configuración de conexión
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN_FLASK = os.getenv("TOKEN_FLASK")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# ==========================================
# Ruta de prueba
# ==========================================
@app.route("/")
def home():
    return {"status": "API DIFODS activa ✅"}

# ==========================================
# Endpoint principal: recibir formulario
# ==========================================
@app.route("/api/formulario", methods=["POST"])
def recibir_formulario():
    try:
        # ================================
        # Verificación de token
        # ================================
        token_cliente = request.headers.get("Authorization")
        if token_cliente != f"Bearer {TOKEN_FLASK}":
            return jsonify({"ok": False, "error": "Acceso no autorizado"}), 401

        # ================================
        # Datos recibidos desde Apps Script
        # ================================
        data = request.get_json()

        Cod_formulario = data.get("Cod_formulario")
        Dni = data.get("Dni")
        Timestamp = data.get("Timestamp")
        Tipo_documento = data.get("Tipo_documento")
        Nombres_y_apellidos = data.get("Nombres_y_apellidos")
        Correo = data.get("Correo")
        N_celular = data.get("N_celular")
        Categoria = data.get("Categoria")
        Sub_categoria = data.get("Sub_categoria")
        Descripcion_consulta = data.get("Descripcion_consulta")
        Ticket = data.get("Ticket")
        Consulta = data.get("Consulta")
        Estado = data.get("Estado")
        Responsable_envio_correo = data.get("Responsable_envio_correo")
        Respuesta = data.get("Respuesta")

        # ================================
        # 🗄️ Insertar registro en PostgreSQL
        # ================================
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO RegistroFormularios (
                Cod_formulario, Dni, Timestamp, Tipo_documento, Nombres_y_apellidos,
                Correo, N_celular, Categoria, Sub_categoria, Descripcion_consulta,
                Ticket, Consulta, Estado, Responsable_envio_correo, Respuesta
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING Id;
        """, (
            Cod_formulario, Dni, Timestamp, Tipo_documento, Nombres_y_apellidos,
            Correo, N_celular, Categoria, Sub_categoria, Descripcion_consulta,
            Ticket, Consulta, Estado, Responsable_envio_correo, Respuesta
        ))

        nuevo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        # ================================
        # ✅ Respuesta al cliente (Apps Script)
        # ================================
        return jsonify({
            "ok": True,
            "msg": "Formulario registrado correctamente ✅",
            "id_generado": nuevo_id
        }), 201

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"ok": False, "error": str(e)}), 500

# ================================================
# Ejecutar localmente
# ================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
