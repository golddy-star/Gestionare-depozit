import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        database=os.getenv('DB_NAME', 'depozit_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASS')
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.cod_sku, p.nume, p.pret_unitar, c.nume as categorie
        FROM produse p 
        LEFT JOIN categorii c ON p.categorie_id = c.id 
        ORDER BY p.id;
    """)
    produse = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', produse=produse)

@app.route('/adauga', methods=['GET', 'POST'])
def adauga():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        sku = request.form.get('sku')
        nume = request.form.get('nume')
        pret = request.form.get('pret')
        categorie_id = request.form.get('categorie')
        categorie_noua = request.form.get('categorie_noua')
        
        # Dacă utilizatorul a scris o categorie nouă în câmpul text
        if categorie_noua and categorie_noua.strip() != "":
            # Creăm categoria și preluăm automat noul ID generat de PostgreSQL
            cur.execute('INSERT INTO categorii (nume) VALUES (%s) RETURNING id', (categorie_noua.strip(),))
            categorie_id = cur.fetchone()[0]
        elif not categorie_id: 
            categorie_id = None
            
        cur.execute('INSERT INTO produse (cod_sku, nume, pret_unitar, categorie_id) VALUES (%s, %s, %s, %s)', 
                    (sku, nume, pret, categorie_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    
    cur.execute('SELECT id, nume FROM categorii ORDER BY nume')
    categorii = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('adauga.html', categorii=categorii)

@app.route('/editeaza/<int:id>', methods=['GET', 'POST'])
def editeaza(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        sku = request.form.get('sku')
        nume = request.form.get('nume')
        pret = request.form.get('pret')
        categorie_id = request.form.get('categorie')
        categorie_noua = request.form.get('categorie_noua')
        
        if categorie_noua and categorie_noua.strip() != "":
            cur.execute('INSERT INTO categorii (nume) VALUES (%s) RETURNING id', (categorie_noua.strip(),))
            categorie_id = cur.fetchone()[0]
        elif not categorie_id: 
            categorie_id = None
            
        cur.execute('UPDATE produse SET cod_sku = %s, nume = %s, pret_unitar = %s, categorie_id = %s WHERE id = %s', 
                    (sku, nume, pret, categorie_id, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    
    cur.execute('SELECT id, cod_sku, nume, pret_unitar, categorie_id FROM produse WHERE id = %s', (id,))
    produs = cur.fetchone()
    
    cur.execute('SELECT id, nume FROM categorii ORDER BY nume')
    lista_categorii = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('editeaza.html', produs=produs, categorii=lista_categorii)

@app.route('/sterge/<int:id>', methods=['POST'])
def sterge(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM produse WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)