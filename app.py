from flask import Flask, request, jsonify, render_template, session
#from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_mysqldb import MySQL
from time import sleep


#csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = "k#s!k#di//e(i4?&?85+u85*uu4--3+9r39##84r|3#$kkkey==/"
# csrf.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS HEADERS'] = 'Content-Type'
# Mysql Connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ventas'
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("/home/index.html")


@app.route('/usuarios', methods=['POST', 'GET'])
def usuarios():
    # if 'id' in session:
    #     print("Hay session: "+str(session['id']))
    # else:
    #     print("No hay session")
    json = []
    status = 499
    if request.method == "POST":
        #user = request.form['user']
        user = request.get_json(force=True)
        print(user)
        #passwd = request.form['password']
        #user = user.replace("'", '').replace("=", "").replace("&", "").replace("|", "")
        #passwd = passwd.replace("'", '').replace("=", "").replace("&", "").replace("|", "")
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuario WHERE `nombres` = %s",
                    (user['user'],))
        data = con.fetchall()
        con.close()
        jsonfy = {}

        #logged = False
        for linea in data:
            id = linea[0]
            nombres = linea[1]
            email = linea[2]
            edad = linea[3]
            telefono = linea[4]
            tipo_doc = linea[5]
            numerodo = linea[6]
            tipous = linea[7]
            imagen_usuario = linea[8]
            passwd = linea[9]
            jsonfy = {
                "status": 200, "user": {
                    "id": id, "nombres": nombres, "email": email, "edad": edad, "telefono": telefono, "tipo_doc": tipo_doc,
                    "numerodo": numerodo, "tipous": tipous, "imagen_usuario": imagen_usuario, "passwd": passwd
                }
            }
            status = 200
            # if (usuario == user or correo == user) and password == passwd:
            #logged = True
            # break
        # if logged == True:
            #json = {"logged": logged, "msg": "Allow", "status": 200}
            #session['id'] = identificador
        # else:
            #jsonfy = {"status": 499, "msg": "Access only for method POST"}
    else:
        #json = {"logged": False, "msg": "Method not permited", "status": 200}
        jsonfy = {"status": 499, "msg": "Access only for method POST"}
    return jsonify(jsonfy), status


if __name__ == "__main__":
    app.run(debug=True, port=8080)
