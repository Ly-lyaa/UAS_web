from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)  # Inisialisasi aplikasi Flask

# Fungsi untuk koneksi ke database MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="lcwproject.mysql.pythonanywhere-services.com",  # Host database di PythonAnywhere
        user="lcwproject",  # Username PythonAnywhere
        password="kipas lucu",  # Password database
        database="lcwproject$skincare_db"  # Nama database di PythonAnywhere
    )

# Fungsi untuk mendapatkan rekomendasi produk
def get_recommendations(skin_type, skin_problem):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT name, description 
    FROM products 
    WHERE skin_type = %s AND skin_problem = %s
    """
    cursor.execute(query, (skin_type, skin_problem))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('index.html')  # Render halaman input

@app.route('/recommend', methods=['POST'])
def recommend():
    # Ambil data dari form
    skin_type = request.form['skin_type']
    skin_problem = request.form['skin_problem']
    
    # Ambil rekomendasi produk dari database
    recommendations = get_recommendations(skin_type, skin_problem)
    
    # Render hasil ke halaman result.html
    return render_template('result.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)  # Jalankan aplikasi di mode debug (hanya untuk lokal)
