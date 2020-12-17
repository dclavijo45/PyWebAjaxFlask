from flask import Flask, request, jsonify, render_template, session
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_mysqldb import MySQL
from time import sleep


csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = "k#s!k#di//e(i4?&?85+u85*uu4--3+9r39##84r|3#$kkkey==/"
csrf.init_app(app)

# Mysql Connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agenda'
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("/home/index.html")


@app.route('/usuarios', methods=['POST', 'GET'])
def usuarios():
    if 'id' in session:
        print("Hay session: "+str(session['id']))
    else:
        print("No hay session")
    json = []
    if request.method == "POST":
        user = request.form['user']
        passwd = request.form['password']
        user = user.replace("'", '').replace(
            "=", "").replace("&", "").replace("|", "")
        passwd = passwd.replace("'", '').replace(
            "=", "").replace("&", "").replace("|", "")
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios")
        data = con.fetchall()
        con.close()

        logged = False
        for linea in data:
            usuario = linea[3]
            password = linea[4]
            correo = linea[2]
            identificador = linea[0]
            if (usuario == user or correo == user) and password == passwd:
                logged = True
                break
        if logged == True:
            json = {"logged": logged, "msg": "Allow", "status": 200}
            session['id'] = identificador
        else:
            json = {"logged": logged, "msg": "Deny", "status": 200}
    else:
        json = {"logged": False, "msg": "Method not permited", "status": 200}
    sleep(1)
    return jsonify(json), 200


if __name__ == "__main__":
    app.run(debug=True, port=80)
