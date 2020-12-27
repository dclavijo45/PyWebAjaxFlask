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
        session.pop('id', None)
    return render_template('/home/register.html')

@app.route("/cpadmin")
def accessAdmin():
    if "id" in session:
        sesionActual = session['id']
        logged = False
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios WHERE id = %s",(sesionActual,))
        data = con.fetchall()
        con.close()
        jsonfy = {}
        for col in data:
            id = col[0]
            if id == sesionActual:
                jsonfy = {"status": 200, "msg": "Sesión iniciada", "Logged": True}
                logged = True
                session["id"] = id
                con2 = mysql.connection.cursor()
                con2.execute("SELECT * FROM clientes WHERE creador_cliente = %s",(sesionActual,))
                data2 = con2.fetchall()
                con2.close()
                if len(data2) == 0:
                    userinfo  = {
                        "username": col[1],
                        "lastname": col[2],
                        "profile_image": col[6],
                        "customers": {
                            "status": False,
                            "id": [],
                            "total": 0,
                            "name": [],
                            "lastname": [],
                            "email": [],
                            "profile_image": [],
                            "client_status": []
                        },
                        "reports": {
                            "status": False
                        }
                    }
                else:
                    # region clientes
                    idcus = []
                    namecus = []
                    lastnamecus = []
                    emailcus = []
                    profile_imagecus = []
                    client_statuscus = []
                    totalcus = 0
                    for cus in data2:
                        idcus.append(cus[0])
                        namecus.append(cus[1])
                        lastnamecus.append(cus[2])
                        emailcus.append(cus[5])
                        profile_imagecus.append(cus[6])
                        client_statuscus.append(cus[8])
                        totalcus+= 1 
                    #endregion

                    # region reportes
                    id_reporte = []
                    clientes_cus = []
                    nombres_cus = []
                    apellidos_cus = []
                    volumen_ventas = []
                    precio_producto_vendido = []
                    fecha_reportecus = []
                    estado_cliente_cus = []
                    
                    con3 = mysql.connection.cursor()
                    con3.execute("SELECT r.id as id_reporte, r.usuario_reportado, r.cantidad_venta, r.fecha_actualizacion, c.nombres, c.apellidos, c.estado_cliente, p.precio_producto * r.cantidad_venta as valor_total from reportes r, clientes c, productos p where ( ( month(r.fecha_actualizacion) = month(DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY)) and (day(r.fecha_actualizacion) >= day(DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY)) and day(r.fecha_actualizacion) <= (day(DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY)) + 6) ) and year(r.fecha_actualizacion) = year(DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY))) ) and r.usuario_reportador = %s and c.producto_asociado = p.id and r.usuario_reportado = c.id ORDER BY day(r.fecha_actualizacion) ASC;",(sesionActual,))
                    data3 = con3.fetchall()
                    con3.close()
                    #endregion

                    #region Revisar si existen reportes
                    if len(data3) != 0:
                        for colx in data3:
                            id_reporte.append(colx[0])
                            clientes_cus.append(colx[1])
                            nombres_cus.append(colx[4])
                            apellidos_cus.append(colx[5])
                            volumen_ventas.append(colx[2])
                            fecha_reportecus.append(colx[3])
                            estado_cliente_cus.append(colx[6])
                            precio_producto_vendido.append(colx[7])

                        userinfo  = {
                            "customers": {
                                "status": True,
                                "total": totalcus,
                                "id": idcus,
                                "name": namecus,
                                "lastname": lastnamecus,
                                "email": emailcus,
                                "profile_image": profile_imagecus,
                                "client_status": client_statuscus
                                },
                                "reports": {
                                    "status": True,
                                    "id_reporte": id_reporte,
                                    "id_customer": clientes_cus,
                                    "name": nombres_cus,
                                    "lastname":apellidos_cus,
                                    "volumen": volumen_ventas,
                                    "precio_producto_vendido": precio_producto_vendido,
                                    "report_date": fecha_reportecus,
                                    "customer_status": estado_cliente_cus
                                },
                                "username": col[1],
                                "lastname": col[2],
                                "profile_image": col[6]
                            }
                    else:
                        userinfo  = {
                            "customers": {
                                "status": True,
                                "total": totalcus,
                                "id": idcus,
                                "name": namecus,
                                "lastname": lastnamecus,
                                "email": emailcus,
                                "profile_image": profile_imagecus,
                                "client_status": client_statuscus
                                },
                                "reports": {
                                    "status": False,
                                    "id_reporte": [],
                                    "id_customer": [],
                                    "name": [],
                                    "lastname":[],
                                    "volumen": [],
                                    "precio_producto_vendido": [],
                                    "report_date": [],
                                    "customer_status": []
                                },
                                "username": col[1],
                                "lastname": col[2],
                                "profile_image": col[6]
                            }
                    #endregion
        
        if logged != True:
            return redirect(url_for('index'))
        return render_template("/admin/cpAdmin.html", userinfo = json.dumps(userinfo, ensure_ascii=False), status = json.dumps(jsonfy, ensure_ascii=False))
    else:
        return "Not logged"

@app.route('/cpacustomers')
def cpaCustomers():
    return "Building..."

@app.route("/logout")
def logoutUser():
    if 'id' in session:
        session.pop('id', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=80)
