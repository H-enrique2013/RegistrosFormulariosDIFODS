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
# ⚙️ Configuración de conexión
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN_FLASK = os.getenv("TOKEN_FLASK")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# ==========================================
# 🧠 Ruta de prueba
# ==========================================
@app.route("/")
def home():
    return {"status": "API DIFODS activa ✅"}

# ==========================================
# 📩 Endpoint principal: recibir formulario
# ==========================================
@app.route("/api/formulario", methods=["POST"])
def recibir_formulario():
    try:
        # ================================
        # 🔒 Verificación de token
        # ================================
        token_cliente = request.headers.get("Authorization")
        if token_cliente != f"Bearer {TOKEN_FLASK}":
            return jsonify({"ok": False, "error": "Acceso no autorizado"}), 401

        # ================================
        # 🧾 Datos recibidos desde Apps Script
        # ================================
        data = request.get_json()

        Cod_formulario = data.get("Cod_formulario")
        Marca_temporal = data.get("Marca_temporal")
        Tipo_documento = data.get("Tipo_documento")
        Num_doc = data.get("Num_doc")
        Nom_apell = data.get("Nom_apell")
        Correo_elec = data.get("Correo_elec")
        Numero_cel = data.get("Numero_cel")
        T0 = data.get("T0")
        T1 = data.get("T1")
        T2 = data.get("T2")
        T3 = data.get("T3")
        T4 = data.get("T4")
        T5 = data.get("T5")
        T6 = data.get("T6")
        T7 = data.get("T7")

        # ================================
        # 🗄️ Insertar registro en PostgreSQL
        # ================================
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO RegistroFormularios (
                Cod_formulario, Marca_temporal, Tipo_documento, Num_doc, Nom_apell,
                Correo_elec, Numero_cel, T0, T1, T2, T3, T4, T5, T6, T7
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING Id;
        """, (
            Cod_formulario, Marca_temporal, Tipo_documento, Num_doc, Nom_apell,
            Correo_elec, Numero_cel, T0, T1, T2, T3, T4, T5, T6, T7
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
# 🚀 Ejecutar localmente
# ================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
