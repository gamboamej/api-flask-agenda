
from flask import Flask, render_template, request, redirect
import pymysql

agenda = Flask(__name__)

def connection():
    s = 'localhost' # servidor
    d = 'dbd_flask_agenda' # base de datos
    u = 'root' # usuario
    p = 'root=2021' # password
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn

# ruta inicio de la agenda
@agenda.route("/")
def main():
    contactos = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("select * from contactos")
    for row in cursor.fetchall():
        contactos.append({"id": row[0], "txnombre": row[1], "txdni": row[2], "txcorreo": row[3],"txtelefono": row[4]})
    conn.close()
    return render_template("contactos.html", contactos = contactos)

# ruta agregar nuevo contacto de la agenda
@agenda.route("/add", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("add.html", contacto = {})
    if request.method == 'POST':
        txnombre = request.form["txnombre"]
        txdni = request.form["txdni"]
        txcorreo = request.form["txcorreo"]
        txtelefono = request.form["txtelefono"]
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contactos (id, txnombre, txdni, txcorreo, txtelefono) VALUES (%s, %s, %s, %s, %s)", (None, txnombre, txdni, txcorreo,txtelefono))
        conn.commit()
        conn.close()
        return redirect('/')

# ruta agregar editar contacto de la agenda
@agenda.route('/upd/<int:id>',methods = ['GET','POST'])
def updatecar(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM contactos WHERE id = %s", (id))
        for row in cursor.fetchall():
            cr.append({"id": row[0], "txnombre": row[1], "txdni": row[2], "txcorreo": row[3],"txtelefono": row[4]})
        conn.close()
        return render_template("add.html", contacto = cr[0])
    if request.method == 'POST':
        txnombre = request.form["txnombre"]
        txdni = request.form["txdni"]
        txcorreo = request.form["txcorreo"]
        txtelefono = request.form["txtelefono"]
        cursor.execute("UPDATE contactos SET txnombre = %s, txdni = %s, txcorreo = %s, txtelefono = %s WHERE id = %s", (txnombre, txdni, txcorreo,txtelefono, id))
        conn.commit()
        conn.close()
        return redirect('/')

# ruta eliminar editar contacto de la agenda
@agenda.route('/del/<int:id>')
def deletecar(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contactos WHERE id = %s", (id))
    conn.commit()
    conn.close()
    return redirect('/')

# comando inicio de app
if(__name__ == "__main__"):
    agenda.run()