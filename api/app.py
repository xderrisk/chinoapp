# app.py
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# --- Database Configuration ---
# IMPORTANT: Replace with your actual MySQL credentials
DB_CONFIG = {
    'host': '172.17.0.1',  # Or your MySQL server IP/hostname
    'user': 'root',
    'password': 'root',
    'database': 'salonesdb'
}

# --- Database Connection Function ---
def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print(f"Successfully connected to MySQL database: {DB_CONFIG['database']}")
        return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# --- API Endpoints ---

@app.route('/aulas', methods=['GET'])
def get_all_aulas():
    """
    Retrieves all classrooms from the 'aulas' table.
    Returns a JSON list of classroom objects.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True) # Use dictionary=True to get results as dictionaries
        cursor.execute("SELECT id_aula, ip_aula, estado FROM aulas")
        aulas = cursor.fetchall()
        return jsonify(aulas), 200
    except Error as e:
        print(f"Error fetching aulas: {e}")
        return jsonify({"error": f"Error fetching data: {e}"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/aulas/<int:id_aula>', methods=['GET'])
def get_aula_by_id(id_aula):
    """
    Retrieves a single classroom by its ID.
    Returns the classroom object if found, otherwise 404.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_aula, ip_aula, estado FROM aulas WHERE id_aula = %s", (id_aula,))
        aula = cursor.fetchone()

        if aula:
            return jsonify(aula), 200
        else:
            return jsonify({"message": "Classroom not found"}), 404
    except Error as e:
        print(f"Error fetching aula by ID: {e}")
        return jsonify({"error": f"Error fetching data: {e}"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/aulas', methods=['POST'])
def add_aula():
    """
    Adds a new classroom to the 'aulas' table.
    Expects JSON data with 'id_aula', 'ip_aula', 'estado'.
    Returns the newly created classroom object and a success message.
    """
    new_aula = request.get_json()
    if not new_aula or not all(k in new_aula for k in ('id_aula', 'ip_aula', 'estado')):
        return jsonify({"error": "Missing data. Required fields: id_aula, ip_aula, estado"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        # Check if id_aula already exists to prevent duplicate primary keys
        cursor.execute("SELECT id_aula FROM aulas WHERE id_aula = %s", (new_aula['id_aula'],))
        if cursor.fetchone():
            return jsonify({"error": f"Classroom with ID {new_aula['id_aula']} already exists"}), 409 # Conflict

        sql = "INSERT INTO aulas (id_aula, ip_aula, estado) VALUES (%s, %s, %s)"
        val = (new_aula['id_aula'], new_aula['ip_aula'], new_aula['estado'])
        cursor.execute(sql, val)
        conn.commit() # Commit the transaction

        return jsonify({"message": "Classroom added successfully", "aula": new_aula}), 201 # 201 Created
    except Error as e:
        print(f"Error adding aula: {e}")
        return jsonify({"error": f"Error adding classroom: {e}"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/aulas/<int:id_aula>', methods=['PUT'])
def update_aula(id_aula):
    """
    Updates an existing classroom by its ID.
    Expects JSON data with 'ip_aula' and/or 'estado'.
    Returns the updated classroom object and a success message.
    """
    updated_data = request.get_json()
    if not updated_data:
        return jsonify({"error": "No data provided for update"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        # Build the SQL query dynamically based on provided fields
        set_clauses = []
        values = []

        if 'ip_aula' in updated_data:
            set_clauses.append("ip_aula = %s")
            values.append(updated_data['ip_aula'])
        if 'estado' in updated_data:
            set_clauses.append("estado = %s")
            values.append(updated_data['estado'])

        if not set_clauses:
            return jsonify({"error": "No valid fields to update (ip_aula or estado required)"}), 400

        sql = f"UPDATE aulas SET {', '.join(set_clauses)} WHERE id_aula = %s"
        values.append(id_aula) # Add id_aula to the end of values for the WHERE clause

        cursor.execute(sql, tuple(values))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Classroom not found or no changes made"}), 404
        else:
            # Optionally fetch the updated record to return
            cursor.execute("SELECT id_aula, ip_aula, estado FROM aulas WHERE id_aula = %s", (id_aula,))
            updated_aula = cursor.fetchone()
            return jsonify({"message": "Classroom updated successfully", "aula": updated_aula}), 200
    except Error as e:
        print(f"Error updating aula: {e}")
        return jsonify({"error": f"Error updating classroom: {e}"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/aulas/<int:id_aula>', methods=['DELETE'])
def delete_aula(id_aula):
    """
    Deletes a classroom by its ID.
    Returns a success message if deleted, otherwise 404.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aulas WHERE id_aula = %s", (id_aula,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Classroom not found"}), 404
        else:
            return jsonify({"message": "Classroom deleted successfully"}), 200
    except Error as e:
        print(f"Error deleting aula: {e}")
        return jsonify({"error": f"Error deleting data: {e}"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- Run the Flask Application ---
if __name__ == '__main__':
    # You can set debug=True for development, but set to False for production
    app.run(debug=True, port=5000)
