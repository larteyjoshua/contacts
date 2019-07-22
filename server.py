from flask import *
import os
import sqlite3
from flask_toastr import Toastr

app = Flask(__name__)
toastr = Toastr(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



def create_table():
    print("Creating table...")
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS contact (created_at date, full_name text, tel_number text);")
    conn.commit()

def add_contact_to_db(created_at, full_name, tel_number):
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute("insert into contact values (?, ?, ?)", (created_at, full_name, tel_number))
    conn.commit()
    flash("Contact inserted SUCCESSFULLY", "success")


@app.route('/')
def index():
    conn = sqlite3.connect("contact.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select * from contact")
    rows = c.fetchall()
    return render_template("contact.html", rows=rows)




@app.route('/add_contact')
def add_contact():
    created_at = request.args.get('created_at')
    full_name = request.args.get('full_name')
    tel_number = request.args.get('tel_number')

    print(created_at)
    print(full_name)
    print(tel_number)
    add_contact_to_db(created_at,full_name,tel_number)
    return redirect("/", code=302)
   
'''
@app.route('/')
def index():
    return render_template("contact.html")'''



if __name__ == '__main__':
    app.run()
