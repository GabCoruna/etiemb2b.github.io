from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc
#import pandas as pd

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Clave secreta para la sesión

# Configuración de la base de datos
SERVER   = '88.26.203.158, 4006'
DATABASE = 'dbModaWin'
USERNAME = 'zorrito'
PASSWORD = '1234' 

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connectionString = ("Driver={SQL Server};Server=88.26.203.158, 4006;Database=dbModaWin;UID=sa;PWD=febjumbo;")

try:
    db = pyodbc.connect(connectionString)
    print('Conexión exitosa')
except:
    print('Error al intentar conectarse')

cursor = db.cursor()

# Función para configurar los encabezados de respuesta y evitar el caché del navegador
@app.after_request
def after_request_func(response):
#def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Ruta para el inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #cursor.execute("SELECT * FROM acceso WHERE nombre = %s AND passwd = %s", (username, password))
        cursor.execute("SELECT * FROM acceso WHERE nombre = '" + username + "' AND passwd = '" + password + "'")
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['username'] = user[0]  # Guardamos el nombre de usuario en la sesión
            return redirect(url_for('home'))
        else:
            # return 'Credenciales inválidas. Inténtalo de nuevo.'
            flash('Credenciales inválidas. Por favor, inténtalo de nuevo.', 'error en el acceso')

    #return render_template('login.html')
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# Ruta para la página principal después de iniciar sesión
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/caballero')
def caballero():
    #return render_template('caballero.html')
    if 'loggedin' in session:
        return render_template('caballero.html', username=session['username'])
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
