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

@app.route('/')
def home():
    return 'Chatbot backend is up!'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    reply = dental_ai_response(user_message)
    return jsonify({'response': reply})

@app.route('/clients', methods=['GET'])
def get_clients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientrecords")
        clients = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"clients": clients})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)