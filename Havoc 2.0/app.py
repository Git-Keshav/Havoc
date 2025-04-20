import mysql.connector
import bcrypt
from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.security import check_password_hash

DB_CONFIG = {
    "host": "localhost",
    "port": "YourPort",
    "user": "YourUser",
    "password": "dbPasswrd",
    "database": "Havoc_Pro"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_database():  
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    cursor.close()
    conn.close()


def users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


create_database()
users_table()




app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():    
    return render_template("log_reg.html")

@app.route('/buddies')
def buddies():
    return render_template("buddies.html")

@app.route('/chatroom')
def chatroom():
    return render_template("chatroom.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

def check_login(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print("connected")
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return False

        return check_password_hash(user['password'], password)

    except Exception as e:
        print("Login error:", e)
        return False



@app.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if check_login(username, password):
        return render_template("home.html")
    else:
        return redirect("/register")
    

@app.route("/register", methods=["POST"])
def register_route():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return "Missing fields", 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        conn.commit()
        cursor.close()
        # conn.close()
        return render_template('home.html'), 200
    except mysql.connector.IntegrityError:
        return "Username or Email already exists", 409
    except Exception as e:
        return f"Error: {str(e)}", 500



if __name__ == "__main__":
    app.run(debug=True)




