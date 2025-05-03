from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from chatbot import dental_ai_response

app = Flask(__name__)
CORS(app)

# MySQL connection config from environment variables
db_config = {
    "host": os.environ.get("DB_HOST", "mysql.hostinger.com"),
    "user": os.environ.get("DB_USER", "u589544679_admin"),
    "password": os.environ.get("DB_PASSWORD", "EW8207A.Asaki"),
    "database": os.environ.get("DB_NAME", "u589544679_clinic")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower()

    if "show clients" in user_message or "show data" in user_message:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientrecords")
            clients = cursor.fetchall()
            cursor.close()
            conn.close()

            if not clients:
                return jsonify({'response': 'No client records found.'})

            response_text = "🧾 Client Records:\n"
            for client in clients:
                response_text += f"- {client['id']}: {client['name']} | {client['email']} | {client['phone']}\n"
            return jsonify({'response': response_text})

        except Exception as e:
            return jsonify({'response': f"Error retrieving client data: {str(e)}"})

    # Default to chatbot response
    reply = dental_ai_response(user_message)
    return jsonify({'response': reply})
