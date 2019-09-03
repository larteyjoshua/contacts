from flask import *
import os
import sqlite3
from flask_toastr import Toastr
import requests
import json

app = Flask(__name__)
toastr = Toastr(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



def create_table():
    print("Creating table...")
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS contact (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, created_at date default current_date not null, full_name text, tel_number text, email text)""")
    conn.commit()

print('...inside create db fxn') 

# if not included, creates only DB without any table    
create_table()

    #Entering data from into database
def add_contact_to_db(full_name, tel_number, email):
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute("insert into contact(full_name, tel_number, email) values (?, ?, ?)", (full_name, tel_number, email))
    conn.commit()
    flash("Contact inserted SUCCESSFULLY", "success")
    
    
    

    # Displaying contact 

@app.route('/')
def index():
    conn = sqlite3.connect("contact.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("select * from contact order by id DESC")
    rows = c.fetchall()
    #Api Call and display
    url="https://beta.ourmanna.com/api/v1/get/?format=json"
    r=requests.get(url)
    data =json.loads(r.text)

    print(data["verse"]["details"]["text"])
    print(data["verse"]["details"]["reference"])
    print(data["verse"]["details"]["version"])

    verse=data["verse"]["details"]["text"]
    ref=data["verse"]["details"]["reference"]
    ver=data["verse"]["details"]["version"]
   
    return render_template("contact.html", rows=rows, verse=verse,ref=ref,ver=ver)


#getting Entered data from form

@app.route('/add_contact')
def add_contact():
   
    full_name = request.args.get('full_name')
    tel_number = request.args.get('tel_number')
    email = request.args.get('email')

    print(email)
    print(full_name)
    print(tel_number)
    add_contact_to_db(full_name, tel_number, email)
    return redirect("/", code=302)
   
#Delating contact from database

@app.route('/delete_contact')

def delete_contact():
    id = request.args.get('id')
    print(id)
    conn = sqlite3.connect('contact.db')
    print('connected')
    c = conn.cursor()
    c.execute("DELETE FROM contact WHERE id= ?", (id,))
    conn.commit()
    flash("Contact Deleted SUCCESSFULLY", "success")
    return redirect("/", code=302)


#Updating Contact 

@app.route('/edit_contact')

def edit_contact():
    id = request.args.get('id')
    full_name = request.args.get('full_name')
    tel_number = request.args.get('tel_number')
    email = request.args.get('email')
    print(email)
    print(full_name)
    print(tel_number)
    print(id)

    conn = sqlite3.connect('contact.db')
    print('connected')
    c = conn.cursor()
    c.execute('''UPDATE contact SET full_name = ?, tel_number =?, email =? WHERE id = ?''', (full_name, tel_number, email, id))
    conn.commit()
    flash("Contact Updated SUCCESSFULLY", "success")
    return redirect("/", code=302)
   





if __name__ == '__main__':
    app.run()
