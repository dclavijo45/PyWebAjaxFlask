from flask import Flask, request, jsonify, render_template, session, url_for, json, redirect
#from datetime import *
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
        statusJsonCustomers = True
        statusJsonReportCW = True
        statusJsonReportLW = True
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
                con2.execute("select c.id, c.nombres, c.apellidos, c.alias, c.correo, c.foto_perfil, c.producto_asociado,c.estado_cliente, p.precio_producto from clientes c, productos p where creador_cliente = %s and c.producto_asociado = p.id",(sesionActual,))
                data2 = con2.fetchall()
                con2.close()
                if len(data2) == 0:
                   statusJsonCustomers = False

                # region clientes
                idcus = []
                namecus = []
                lastnamecus = []
                aliascus = []
                emailcus = []
                profile_imagecus = []
                client_statuscus = []
                precio_pago_prodcus = []
                totalcus = 0

                for cus in data2:
                    idcus.append(cus[0])
                    namecus.append(cus[1])
                    lastnamecus.append(cus[2])
                    aliascus.append(cus[3])
                    emailcus.append(cus[4])
                    profile_imagecus.append(cus[5])
                    client_statuscus.append(cus[7])
                    precio_pago_prodcus.append(cus[8])
                    totalcus+= 1 
                #endregion

                # region reportes semana actual
                id_reporte = []
                clientes_cus = []
                nombres_cus = []
                apellidos_cus = []
                volumen_ventas = []
                precio_producto_vendido = []
                fecha_reportecus = []
                estado_cliente_cus = []

                con3 = mysql.connection.cursor()
                con3.execute("SELECT r.id as id_reporte, r.usuario_reportado, r.cantidad_venta, r.fecha_actualizacion, c.nombres, c.apellidos, c.estado_cliente, p.precio_producto * r.cantidad_venta as valor_total from reportes r, clientes c, productos p where (date(r.fecha_actualizacion) >= DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY) and date(r.fecha_actualizacion) <= DATE_ADD(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 6 DAY ) ) and r.usuario_reportador = %s and c.producto_asociado = p.id and r.usuario_reportado = c.id and estado_reporte = 1 ORDER BY day(r.fecha_actualizacion) ASC;",(sesionActual,))
                data3 = con3.fetchall()
                con3.close()
                #endregion

                #region Revisar si existen reportes SM-AC
                if len(data3) == 0:
                    statusJsonReportCW = False

                for colx in data3:
                    id_reporte.append(colx[0])
                    clientes_cus.append(colx[1])
                    nombres_cus.append(colx[4])
                    apellidos_cus.append(colx[5])
                    volumen_ventas.append(colx[2])
                    fecha_reportecus.append(colx[3])
                    estado_cliente_cus.append(colx[6])
                    precio_producto_vendido.append(colx[7])
                    #endregion

                #region reportes semana pasada
                id_reporteSmpa = []
                clientes_cusSmpa = []
                nombres_cusSmpa = []
                apellidos_cusSmpa = []
                volumen_ventasSmpa = []
                precio_producto_vendidoSmpa = []
                fecha_reportecusSmpa = []
                estado_cliente_cusSmpa = []

                con4 = mysql.connection.cursor()
                con4.execute("SELECT r.id as id_reporte, r.usuario_reportado, r.cantidad_venta, r.fecha_actualizacion, c.nombres, c.apellidos, c.estado_cliente, p.precio_producto * r.cantidad_venta as valor_total from reportes r, clientes c, productos p where (date(r.fecha_actualizacion) >= DATE_SUB(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 7 DAY ) and date(r.fecha_actualizacion) <= DATE_SUB(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 1 DAY)) and r.usuario_reportador = %s and c.producto_asociado = p.id and r.usuario_reportado = c.id and estado_reporte = 1 ORDER BY day(r.fecha_actualizacion) ASC;",(sesionActual,))
                data4 = con4.fetchall()
                con4.close()
                #endregion

                #region Revisar si existen reportes SM-PA
                if len(data4) == 0:
                    statusJsonReportLW = False
                
                for colx in data4:
                    id_reporteSmpa.append(colx[0])
                    clientes_cusSmpa.append(colx[1])
                    nombres_cusSmpa.append(colx[4])
                    apellidos_cusSmpa.append(colx[5])
                    volumen_ventasSmpa.append(colx[2])
                    fecha_reportecusSmpa.append(colx[3])
                    estado_cliente_cusSmpa.append(colx[6])
                    precio_producto_vendidoSmpa.append(colx[7])
                #endregion
            
                userinfo  = {
                                    "customers": {
                                        "status": statusJsonCustomers,
                                        "total": totalcus,
                                        "id": idcus,
                                        "name": namecus,
                                        "lastname": lastnamecus,
                                        "alias": aliascus,
                                        "email": emailcus,
                                        "precio_pago_prod": precio_pago_prodcus,
                                        "profile_image": profile_imagecus,
                                        "client_status": client_statuscus
                                        },
                                        "reports": {
                                            "current_week":{
                                                "status": statusJsonReportCW,
                                                "id_reporte": id_reporte,
                                                "id_customer": clientes_cus,
                                                "name": nombres_cus,
                                                "lastname":apellidos_cus,
                                                "volumen": volumen_ventas,
                                                "precio_producto_vendido": precio_producto_vendido,
                                                "report_date": fecha_reportecus,
                                                "customer_status": estado_cliente_cus
                                            },
                                            "last_week": {
                                                "status": statusJsonReportLW,
                                                "id_reporte": id_reporteSmpa,
                                                "id_customer": clientes_cusSmpa,
                                                "name": nombres_cusSmpa,
                                                "lastname":apellidos_cusSmpa,
                                                "volumen": volumen_ventasSmpa,
                                                "precio_producto_vendido": precio_producto_vendidoSmpa,
                                                "report_date": fecha_reportecusSmpa,
                                                "customer_status": estado_cliente_cusSmpa
                                            }
                                        },
                                        "username": col[1],
                                        "lastname": col[2],
                                        "profile_image": col[6]
                                    }
        if logged != True:
            return redirect(url_for('index'))
        
        return render_template("/admin/cpAdmin.html", userinfo = json.dumps(userinfo, ensure_ascii=False), status = json.dumps(jsonfy, ensure_ascii=False))
    else:
        return redirect(url_for('index'))

@app.route('/cpacustomers')
def cpaCustomers():
    return "Building..."

@app.route("/logout")
def logoutUser():
    if 'id' in session:
        session.pop('id', None)
    return redirect(url_for('index'))

@app.route("/apirf", methods = ['PUT','DELETE', 'POST','GET'])
def cpAddReg():
    if "id" in session:
        statusJsonCustomers = True
        statusJsonReportCW = True
        statusJsonReportLW = True
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
                con2 = mysql.connection.cursor()
                con2.execute("select c.id, c.nombres, c.apellidos, c.alias, c.correo, c.foto_perfil, c.producto_asociado,c.estado_cliente, p.precio_producto from clientes c, productos p where creador_cliente = %s and c.producto_asociado = p.id",(sesionActual,))
                data2 = con2.fetchall()
                con2.close()

                if len(data2) == 0:
                   statusJsonCustomers = False
                   return jsonify({"status": 401, "msg": "Action not permitied"}), 401
                
                if request.method == "PUT":
                    datares = request.get_json(force=True)
                    for i in data2:
                        if i[0] == int(datares["IARid"]):
                            conIS = mysql.connection.cursor()
                            conIS.execute("INSERT INTO liveone.reportes(usuario_reportado,usuario_reportador, id_producto, cantidad_venta, fecha_actualizacion, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s)", (datares["IARid"], sesionActual, i[6], datares["IARquantity"], datares["IARdate"], datares["IARdate"]))
                            mysql.connection.commit()
                            conIS.close()
                            break
                elif request.method == "DELETE":
                    datares = request.get_json(force=True)
                    try:
                        conIS = mysql.connection.cursor()
                        conIS.execute("UPDATE reportes SET estado_reporte = 0 WHERE id = %s and usuario_reportador = %s", (datares["id_registro"], sesionActual),) 
                        mysql.connection.commit()
                        conIS.close()
                    except :
                        return redirect(url_for('index'))
                elif request.method == "POST":
                    datares = request.get_json(force=True)
                    for i in data2:
                        if i[0] == int(datares["id_usuario"]):
                            try:
                                conIS = mysql.connection.cursor()
                                conIS.execute("UPDATE reportes SET usuario_reportado = %s, cantidad_venta = %s, fecha_actualizacion = %s WHERE (id = %s) and usuario_reportador = %s", (datares["id_usuario"],datares["volumen"], datares["fecha_act"], datares["id_reporte"], sesionActual))
                                mysql.connection.commit()
                                conIS.close()
                            except :
                                return redirect(url_for('index'))
                            break
                else:
                    return redirect(url_for('index'))
                # region clientes
                    
                idcus = []
                namecus = []
                lastnamecus = []
                aliascus = []
                emailcus = []
                profile_imagecus = []
                client_statuscus = []
                precio_pago_prodcus = []
                totalcus = 0

                for cus in data2:
                    idcus.append(cus[0])
                    namecus.append(cus[1])
                    lastnamecus.append(cus[2])
                    aliascus.append(cus[3])
                    emailcus.append(cus[4])
                    profile_imagecus.append(cus[5])
                    client_statuscus.append(cus[7])
                    precio_pago_prodcus.append(cus[8])
                    totalcus+= 1 
                #endregion

                # region reportes semana actual
                id_reporte = []
                clientes_cus = []
                nombres_cus = []
                apellidos_cus = []
                volumen_ventas = []
                precio_producto_vendido = []
                fecha_reportecus = []
                estado_cliente_cus = []

                con3 = mysql.connection.cursor()
                con3.execute("SELECT r.id as id_reporte, r.usuario_reportado, r.cantidad_venta, r.fecha_actualizacion, c.nombres, c.apellidos, c.estado_cliente, p.precio_producto * r.cantidad_venta as valor_total from reportes r, clientes c, productos p where (date(r.fecha_actualizacion) >= DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY) and date(r.fecha_actualizacion) <= DATE_ADD(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 6 DAY ) ) and r.usuario_reportador = %s and c.producto_asociado = p.id and r.usuario_reportado = c.id and r.estado_reporte = 1 ORDER BY day(r.fecha_actualizacion) ASC;",(sesionActual,))
                data3 = con3.fetchall()
                con3.close()
                #endregion

                #region Revisar si existen reportes SM-AC
                if len(data3) == 0:
                    statusJsonReportCW = False

                for colx in data3:
                    id_reporte.append(colx[0])
                    clientes_cus.append(colx[1])
                    nombres_cus.append(colx[4])
                    apellidos_cus.append(colx[5])
                    volumen_ventas.append(colx[2])
                    fecha_reportecus.append(colx[3])
                    estado_cliente_cus.append(colx[6])
                    precio_producto_vendido.append(colx[7])
                    #endregion

                #region reportes semana pasada
                id_reporteSmpa = []
                clientes_cusSmpa = []
                nombres_cusSmpa = []
                apellidos_cusSmpa = []
                volumen_ventasSmpa = []
                precio_producto_vendidoSmpa = []
                fecha_reportecusSmpa = []
                estado_cliente_cusSmpa = []

                con4 = mysql.connection.cursor()
                con4.execute("SELECT r.id as id_reporte, r.usuario_reportado, r.cantidad_venta, r.fecha_actualizacion, c.nombres, c.apellidos, c.estado_cliente, p.precio_producto * r.cantidad_venta as valor_total from reportes r, clientes c, productos p where (date(r.fecha_actualizacion) >= DATE_SUB(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 7 DAY ) and date(r.fecha_actualizacion) <= DATE_SUB(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 1 DAY)) and r.usuario_reportador = %s and c.producto_asociado = p.id and r.usuario_reportado = c.id and r.estado_reporte = 1 ORDER BY day(r.fecha_actualizacion) ASC;",(sesionActual,))
                data4 = con4.fetchall()
                con4.close()
                #endregion

                #region Revisar si existen reportes SM-PA
                if len(data4) == 0:
                    statusJsonReportLW = False
                
                for colx in data4:
                    id_reporteSmpa.append(colx[0])
                    clientes_cusSmpa.append(colx[1])
                    nombres_cusSmpa.append(colx[4])
                    apellidos_cusSmpa.append(colx[5])
                    volumen_ventasSmpa.append(colx[2])
                    fecha_reportecusSmpa.append(colx[3])
                    estado_cliente_cusSmpa.append(colx[6])
                    precio_producto_vendidoSmpa.append(colx[7])
                #endregion
            
                userinfo  = {
                                    "customers": {
                                        "status": statusJsonCustomers,
                                        "total": totalcus,
                                        "id": idcus,
                                        "name": namecus,
                                        "lastname": lastnamecus,
                                        "alias": aliascus,
                                        "email": emailcus,
                                        "precio_pago_prod": precio_pago_prodcus,
                                        "profile_image": profile_imagecus,
                                        "client_status": client_statuscus
                                        },
                                        "reports": {
                                            "current_week":{
                                                "status": statusJsonReportCW,
                                                "id_reporte": id_reporte,
                                                "id_customer": clientes_cus,
                                                "name": nombres_cus,
                                                "lastname":apellidos_cus,
                                                "volumen": volumen_ventas,
                                                "precio_producto_vendido": precio_producto_vendido,
                                                "report_date": fecha_reportecus,
                                                "customer_status": estado_cliente_cus
                                            },
                                            "last_week": {
                                                "status": statusJsonReportLW,
                                                "id_reporte": id_reporteSmpa,
                                                "id_customer": clientes_cusSmpa,
                                                "name": nombres_cusSmpa,
                                                "lastname":apellidos_cusSmpa,
                                                "volumen": volumen_ventasSmpa,
                                                "precio_producto_vendido": precio_producto_vendidoSmpa,
                                                "report_date": fecha_reportecusSmpa,
                                                "customer_status": estado_cliente_cusSmpa
                                            }
                                        },
                                        "username": col[1],
                                        "lastname": col[2],
                                        "profile_image": col[6]
                                    }
        if logged != True:
            return redirect(url_for('index'))
        else:
            return jsonify(userinfo), 200

if __name__ == "__main__":
    app.run(debug=True, port=80)
