from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'secret123'  # Dibutuhkan untuk flash message

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS vaksin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        tanggal TEXT NOT NULL,
        jenis TEXT NOT NULL,
        tinggi REAL,
        berat REAL
    )""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM vaksin ORDER BY tanggal")
    data = c.fetchall()
    conn.close()

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    # Notifikasi untuk hari ini dan besok
    for row in data:
        tgl_vaksin = datetime.strptime(row[2], '%Y-%m-%d').date()
        if tgl_vaksin == today:
            flash(f"Hari ini jadwal vaksin untuk {row[1]} ({row[3]})")
        elif tgl_vaksin == tomorrow:
            flash(f"Besok jadwal vaksin untuk {row[1]} ({row[3]})")

    return render_template('index.html', data=data, today=today.strftime('%Y-%m-%d'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        tanggal = request.form['tanggal']
        jenis = request.form['jenis']
        tinggi = request.form['tinggi']
        berat = request.form['berat']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO vaksin (nama, tanggal, jenis, tinggi, berat) VALUES (?, ?, ?, ?, ?)", 
                  (nama, tanggal, jenis, tinggi, berat))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM vaksin WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)