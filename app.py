from flask import Flask, request, jsonify, render_template, session, url_for, json, redirect

# from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_mysqldb import MySQL
from time import sleep


# csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = "k#s!k#di//e(i4?&?85+u85*uu4--3+9r39##84r|3#$kkkey==/"
# csrf.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS HEADERS"] = "Content-Type"
# Mysql Connection
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "liveone"
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("/home/index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        sleep(1)
        if "id" in session:
            print("Hay session: " + str(session["id"]))
        logged = False
        jsonfy = {}
        datares = request.get_json(force=True)
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios")
        data = con.fetchall()
        con.close()
        jsonfy = {}
        for col in data:
            id = col[0]
            correo = col[5]
            clave = str(col[8])
            if correo == datares["correo"] and clave == datares["clave"]:
                jsonfy = {"status": 200, "msg": "Sesión iniciada", "Logged": True}
                logged = True
                session["id"] = id
                break
        if logged != True:
            jsonfy = {
                "status": 499,
                "msg": "Usuario o contraseña incorrecto",
                "Logged": False,
            }
    else:
        jsonfy = {"status": 405, "msg": "Access only for method POST", "Logged": False}
    return jsonify(jsonfy), 200


@app.route("/registeruser", methods=['POST', 'GET'])
def registerUser():
    # if 'id' in session:
    #     return url_for('login')
    if request.method == "POST":
        sleep(1)
        if "id" in session:
            print("Hay session: " + str(session["id"]))
        Access = True
        jsonfy = {}
        datares = request.get_json(force=True)
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios")
        data = con.fetchall()
        con.close()
        jsonfy = {}
        for col in data:
            # id = col[0]
            correo = col[5]
            clave = col[4]
            print(datares["clave"])
            if correo == datares["correo"] or clave == str(datares["num_documento"]):
                Access = False
                break
        if Access == False:
            jsonfy = {
                "status": 406,
                "msg": "Ya existe este usuario",
                "Logged": False,
            }
        else:
            conR = mysql.connection.cursor()
            conR.execute("INSERT INTO usuarios (nombres, apellidos, tipo_identificacion, num_identificacion, correo, clave_usuario) VALUES (%s,%s,%s,%s,%s,%s)", (datares["nombres"],datares["apellidos"],datares["tipo_identificacion"],datares["num_documento"],datares["correo"],datares["clave"],))
            mysql.connection.commit()
            if conR.rowcount >= 1:
                conR.close()
                conL = mysql.connection.cursor()
                conL.execute("SELECT id FROM usuarios  WHERE correo=%s",(datares['correo'],))
                dataL = conL.fetchall()
                for col in data:
                    session['id'] = col[0]
                conL.close()
                jsonfy = {
                    "status": 201,
                    "msg": "Registrado correctamente",
                    "Logged": True,
                }
            else:
                jsonfy = {
                    "status": 412,
                    "msg": "Problemas al registrarse",
                    "Logged": False,
                }
                conR.close()

    else:
        jsonfy = {"status": 405, "msg": "Access only for method POST", "Logged": False}
    return jsonify(jsonfy), 200


@app.route("/register", methods=['POST', 'GET'])
def register():
    if 'id' in session:
        return url_for('login')

    return render_template('/home/register.html')

@app.route("/cpadmin")
def accessAdmin():
    if "id" in session:
        usuarioLogueado = ""
        foto_perfil = ""
        sesionActual = session['id']
        logged = False
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios WHERE id = %s",(sesionActual,))
        data = con.fetchall()
        con.close()
        jsonfy = {}
        for col in data:
            id = col[0]
            foto_perfil = col[6]
            if id == sesionActual:
                usuarioLogueado = col[1]
                jsonfy = {"status": 200, "msg": "Sesión iniciada", "Logged": True}
                logged = True
                session["id"] = id
                break
        if logged != True:
            jsonfy = {
                "status": 499,
                "msg": "Usuario o contraseña incorrecto",
                "Logged": False,
            }
            return url_for('login')
        return render_template("/admin/cpAdmin.html", foto_perfil = foto_perfil, usuario=usuarioLogueado, status = json.dumps(jsonfy, ensure_ascii=False))
    else:
        return "Not logged"

@app.route("/logout")
def logoutUser():
    if 'id' in session:
        session.pop('id', None)
    return redirect(url_for('index'))

@app.route("/testc")
def testChart():
    return render_template("/admin/chartTest.html")

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=80)
