from flask import *
import os
import sqlite3

app = Flask(__name__)

def create_table():
    print("Creating table...")
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS contact (created_at date, full_name text, tel_number text);")
    conn.commit()

def get_contact_from_db():
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute("SELECT created_at,full_name,tel_number FROM contact;")
    return list(map(lambda row: row[0], c.fetchall()))

def add_contact_to_db(created_at, full_name, tel_number):
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute("INSERT INTO contact VALUES ('" + created_at + "," + full_name + ", " + tel_number + "');")
    conn.commit()

@app.route('/')
def index():
    created_at = get_contact_from_db()
    full_name = get_contact_from_db()
    tel_number = get_contact_from_db()
    return render_template('contact.html', created_at=created_at,full_name=full_name,tel_number=tel_number)

@app.route('/add_contact')
def add_contact():
    created_at = request.args.get('created_at')
    full_name = request.args.get('full_name')
    tel_number = request.args.get('tel_number')

    print(created_at)
    print(full_name)
    print(tel_number)
    add_contact_to_db(created_at)
    add_contact_to_db(full_name)
    add_contact_to_db(tel_number)
    return redirect("/", code=302)

 
@app.route('/')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    create_table()
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0',port=port)