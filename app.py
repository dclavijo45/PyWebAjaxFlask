from flask import Flask, request, jsonify, render_template, session, url_for, json, redirect, abort
# from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_mysqldb import MySQL
from time import sleep
import requests

# csrf = CSRFProtect()
app = Flask(__name__)
port = 80
hostA = '0.0.0.0'
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


def fixStringClient(string):
    fixed = str(string).replace("'", "").replace("*", "").replace('"', "").replace("+", "").replace("|", "").replace("%", "").replace("$", "").replace("&", "").replace("=", "").replace("?", "").replace('¡', "").replace("\a", "").replace("<", "").replace(">", "").replace("/", "").replace("[", "").replace("]", "").replace("(", "").replace("]", "").replace("´", "").replace(",", "").replace("!", "").replace("\n", "")
    return fixed


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("/home/index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
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
                jsonfy = {"status": 200,
                          "msg": "Sesión iniciada", "Logged": True}
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
        jsonfy = {"status": 405,
                  "msg": "Access only for method POST", "Logged": False}
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
            conR.execute("INSERT INTO usuarios (nombres, apellidos, tipo_identificacion, num_identificacion, correo, clave_usuario) VALUES (%s,%s,%s,%s,%s,%s)",
                         (datares["nombres"], datares["apellidos"], datares["tipo_identificacion"], datares["num_documento"], datares["correo"], datares["clave"],))
            mysql.connection.commit()
            if conR.rowcount >= 1:
                conR.close()
                conL = mysql.connection.cursor()
                conL.execute(
                    "SELECT id FROM usuarios  WHERE correo=%s", (datares['correo'],))
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
        jsonfy = {"status": 405,
                  "msg": "Access only for method POST", "Logged": False}
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
        con.execute("SELECT * FROM usuarios WHERE id = %s", (sesionActual,))
        data = con.fetchall()
        con.close()
        jsonfy = {}
        for col in data:
            id = col[0]
            if id == sesionActual:
                jsonfy = {"status": 200,
                          "msg": "Sesión iniciada", "Logged": True}
                logged = True
                urlGet = 'http://localhost:{0}/apirf'.format(port)
                cookies = {'session': request.cookies.get('session')}
                req = requests.get(urlGet, cookies=cookies)
                userinfo = req.json()
        if logged != True:
            return redirect(url_for('index'))

        return render_template("/admin/cpAdmin.html", userinfo=json.dumps(userinfo, ensure_ascii=False), status=json.dumps(jsonfy, ensure_ascii=False))
    else:
        return redirect(url_for('index'))


@app.route('/cpacustomers')
def cpaCustomers():
    if "id" in session:
        sesionActual = session['id']
        logged = False
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios WHERE id = %s", (sesionActual,))
        data = con.fetchall()
        con.close()
        jsonfy = {}
        for col in data:
            id = col[0]
            if id == sesionActual:
                jsonfy = {"status": 200,
                          "msg": "Sesión iniciada", "Logged": True}
                logged = True
                cookies = {'session': request.cookies.get('session')}
                urlRf = 'http://localhost:{0}/apirf'.format(port)
                urlProd = 'http://localhost:{0}/apiprod'.format(port)
                urlCus = 'http://localhost:{0}/apicus'.format(port)
                req = requests.get(urlRf, cookies=cookies)
                req2 = requests.get(urlProd, cookies=cookies)
                req3 = requests.get(urlCus, cookies=cookies)
                userinfo = req.json()
                prodsinfo = req2.json()
                cusinfo = req3.json()

        if logged != True:
            return redirect(url_for('index'))

        return render_template("/admin/cpaCustomers.html", userinfo=json.dumps(userinfo, ensure_ascii=False), status=json.dumps(jsonfy, ensure_ascii=False), prodsinfo=json.dumps(prodsinfo, ensure_ascii=False), cusinfo=json.dumps(cusinfo, ensure_ascii=False))
    else:
        return redirect(url_for('index'))


@app.route("/logout")
def logoutUser():
    if 'id' in session:
        session.pop('id', None)
    return redirect(url_for('index'))


@app.route("/apirf", methods=['PUT', 'DELETE', 'POST', 'GET'])
def manageRegisterInfo():
    if "id" in session:
        statusJsonCustomers = True
        statusJsonReportCW = True
        statusJsonReportLW = True
        sesionActual = session['id']
        logged = False
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios WHERE id = %s", (sesionActual,))
        data = con.fetchall()
        con.close()
        for col in data:
            id = col[0]
            if id == sesionActual:
                logged = True
                con2 = mysql.connection.cursor()
                con2.execute("select c.id, c.nombres, c.apellidos, c.alias, c.correo, c.foto_perfil, c.producto_asociado,c.estado_cliente, p.precio_producto from clientes c, productos p where creador_cliente = %s and c.producto_asociado = p.id", (sesionActual,))
                data2 = con2.fetchall()
                con2.close()

                if request.method == "POST":
                    datares = request.get_json(force=True)
                    for i in data2:
                        if i[0] == int(datares["IARid"]):
                            conIS = mysql.connection.cursor()
                            conIS.execute("INSERT INTO liveone.reportes(usuario_reportado,usuario_reportador, id_producto, cantidad_venta, fecha_actualizacion, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s)", (
                                datares["IARid"], sesionActual, i[6], datares["IARquantity"], datares["IARdate"], datares["IARdate"]))
                            mysql.connection.commit()
                            conIS.close()
                            break
                elif request.method == "DELETE":
                    datares = request.get_json(force=True)
                    try:
                        conIS = mysql.connection.cursor()
                        conIS.execute("UPDATE reportes SET estado_reporte = 0 WHERE id = %s and usuario_reportador = %s", (
                            datares["id_registro"], sesionActual),)
                        mysql.connection.commit()
                        conIS.close()
                    except:
                        return redirect(url_for('index'))
                elif request.method == "PUT":  # ??
                    datares = request.get_json(force=True)
                    for i in data2:
                        if i[0] == int(datares["id_usuario"]):
                            try:
                                conIS = mysql.connection.cursor()
                                conIS.execute("UPDATE reportes SET usuario_reportado = %s, cantidad_venta = %s, fecha_actualizacion = %s WHERE (id = %s) and usuario_reportador = %s", (
                                    datares["id_usuario"], datares["volumen"], datares["fecha_act"], datares["id_reporte"], sesionActual))
                                mysql.connection.commit()
                                conIS.close()
                            except:
                                return redirect(url_for('index'))
                            break
                else:
                    pass
                    # datares = request.get_json(force=True)
                    # if datares["refresh"] == True:
                    #     pass
                    # else:
                    #     return redirect(url_for('index'))

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
                    totalcus += 1
                # endregion

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
                con3.execute("SELECT r.id as id_reporte, r.usuario_reportado, r.cantidad_venta, r.fecha_actualizacion, c.nombres, c.apellidos, c.estado_cliente, p.precio_producto * r.cantidad_venta as valor_total from reportes r, clientes c, productos p where (date(r.fecha_actualizacion) >= DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY) and date(r.fecha_actualizacion) <= DATE_ADD(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 6 DAY ) ) and r.usuario_reportador = %s and c.producto_asociado = p.id and r.usuario_reportado = c.id and r.estado_reporte = 1 ORDER BY day(r.fecha_actualizacion) ASC;", (sesionActual,))
                data3 = con3.fetchall()
                con3.close()
                # endregion

                # region Revisar si existen reportes SM-AC
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
                    # endregion

                # region reportes semana pasada
                id_reporteSmpa = []
                clientes_cusSmpa = []
                nombres_cusSmpa = []
                apellidos_cusSmpa = []
                volumen_ventasSmpa = []
                precio_producto_vendidoSmpa = []
                fecha_reportecusSmpa = []
                estado_cliente_cusSmpa = []

                con4 = mysql.connection.cursor()
                con4.execute("SELECT r.id as id_reporte, r.usuario_reportado, r.cantidad_venta, r.fecha_actualizacion, c.nombres, c.apellidos, c.estado_cliente, p.precio_producto * r.cantidad_venta as valor_total from reportes r, clientes c, productos p where (date(r.fecha_actualizacion) >= DATE_SUB(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 7 DAY ) and date(r.fecha_actualizacion) <= DATE_SUB(DATE_ADD(curdate(), INTERVAL - WEEKDAY(CURDATE()) DAY), INTERVAL 1 DAY)) and r.usuario_reportador = %s and c.producto_asociado = p.id and r.usuario_reportado = c.id and r.estado_reporte = 1 ORDER BY day(r.fecha_actualizacion) ASC;", (sesionActual,))
                data4 = con4.fetchall()
                con4.close()
                # endregion

                # region Revisar si existen reportes SM-PA
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
                # endregion

                userinfo = {
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
                        "current_week": {
                            "status": statusJsonReportCW,
                            "id_reporte": id_reporte,
                            "id_customer": clientes_cus,
                            "name": nombres_cus,
                            "lastname": apellidos_cus,
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
                            "lastname": apellidos_cusSmpa,
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
    else:
        return redirect(url_for('index'))


@app.route('/apicus', methods=['PUT', 'DELETE', 'POST', 'GET'])
def manageCustomers():
    if 'id' in session:
        sesionActual = session['id']
        propietario = False
        logged = False
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios WHERE id = %s", (sesionActual,))
        data = con.fetchall()
        con.close()
        for col in data:
            id = col[0]
            if id == sesionActual:
                logged = True

                # region API REST
                if request.method == 'POST':
                    dataR = request.get_json(force=True)
                    if len(dataR["nombreCliente"]) == 0 or len(dataR["apellidoCliente"]) == 0 or len(dataR["tipoIdCliente"]) == 0 or len(dataR["numDocumentoCliente"]) == 0 or len(dataR["productoAsignadoCliente"]) == 0:
                        pass
                    else:
                        if len(dataR["aliasCliente"]) == 0:
                            dataR["aliasCliente"] = "sin alias"
                        if len(dataR["correoCliente"]) == 0:
                            dataR["correoCliente"] = "sin correo"
                        
                        productoAsignado = fixStringClient(dataR["productoAsignadoCliente"])
                        conV = mysql.connection.cursor()
                        conV.execute("SELECT creador_producto FROM productos WHERE id = %s", (productoAsignado))
                        dataV = conV.fetchall()
                        conV.close()
                        for val in dataV:
                            if str(val[0]) == str(productoAsignado):
                                propietario = True
                                break
                        if propietario == True:
                            conx1 = mysql.connection.cursor()
                            conx1.execute("INSERT INTO `clientes` (`nombres`, `apellidos`, `alias`, `tipo_identificacion`, `num_identificacion`, `correo`, `producto_asociado`, `creador_cliente`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (
                                fixStringClient(dataR["nombreCliente"]),
                                fixStringClient(dataR["apellidoCliente"]), fixStringClient(dataR["aliasCliente"]),
                                fixStringClient(dataR["tipoIdCliente"]),
                                fixStringClient(dataR["numDocumentoCliente"]),
                                fixStringClient(dataR["correoCliente"]),
                                fixStringClient(dataR["productoAsignadoCliente"]),
                                sesionActual,
                            ))
                            mysql.connection.commit()
                            conx1.close()
                        else:
                            pass
                elif request.method == "GET":
                    pass
                elif request.method == "PUT":
                    pass
                elif request.method == "DELETE":
                    pass
                else:
                    return redirect(url_for('index'))
                # endregion

                # region sistema de exportación de usuarios
                id_customerR = []
                nombre_customerR = []
                apellidos_customerR = []
                alias_customerR = []
                tipo_identificacion_customerR = []
                num_identificacion_customerR = []
                correo_customerR = []
                foto_perfil_customerR = []
                nombre_producto_customerR = []
                estado_customerR = []
                id_producto_customerR = []
                precio_producto_customerR = []

                con2 = mysql.connection.cursor()
                con2.execute("SELECT c.id, c.nombres, c.apellidos, c.alias, c.tipo_identificacion, c.num_identificacion,c.correo, c.foto_perfil, p.nombre_producto as producto_asociado, c.estado_cliente, p.id as id_producto, p.precio_producto as precio_producto FROM clientes c, productos p where c.producto_asociado=p.id and c.creador_cliente = %s", (sesionActual,))
                data2 = con2.fetchall()
                con2.close()

                for col2 in data2:
                    if col2[9] != 2:
                        id_customerR.append(col2[0])
                        nombre_customerR.append(col2[1])
                        apellidos_customerR.append(col2[2])
                        alias_customerR.append(col2[3])
                        tipo_identificacion_customerR.append(col2[4])
                        num_identificacion_customerR.append(col2[5])
                        correo_customerR.append(col2[6])
                        foto_perfil_customerR.append(col2[7])
                        nombre_producto_customerR.append(col2[8])
                        estado_customerR.append(col2[9])
                        id_producto_customerR.append(col2[10])
                        precio_producto_customerR.append(col2[11])

                Customers = {
                    "id_cliente": id_customerR,
                    "nombres": nombre_customerR,
                    "apellidos": apellidos_customerR,
                    "alias": alias_customerR,
                    "tipo_identificacion": tipo_identificacion_customerR,
                    "numero_identificacion": num_identificacion_customerR,
                    "correo": correo_customerR,
                    "foto_perfil": foto_perfil_customerR,
                    "nombre_producto_asociado": nombre_producto_customerR,
                    "estado_cliente": estado_customerR,
                    "id_producto_asociado": id_producto_customerR,
                    "precio_producto_asociado": precio_producto_customerR
                }
                # endregion
        if logged != True:
            return redirect(url_for('index'))
        else:
            return jsonify(Customers), 200

    else:
        return redirect(url_for('index'))


@app.route('/apiprod', methods=['PUT', 'DELETE', 'POST', 'GET'])
def manageProducts():
    if 'id' in session:
        sesionActual = session['id']
        logged = False
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM usuarios WHERE id = %s", (sesionActual,))
        data = con.fetchall()
        con.close()
        for col in data:
            id = col[0]
            if id == sesionActual:
                logged = True

                # region sistema de exportación de usuarios
                id_producto = []
                nombre_producto = []
                descripcion_producto = []
                imagen_producto = []
                precio_producto = []
                cantidad_producto = []
                observaciones_producto = []
                fecha_creacion_producto = []
                fecha_actualizacion_producto = []
                estado_producto = []

                con2 = mysql.connection.cursor()
                con2.execute(
                    "SELECT * FROM productos WHERE creador_producto = %s;", (sesionActual,))
                data2 = con2.fetchall()
                con2.close()

                for col2 in data2:
                    if col2[10] == 1:
                        id_producto.append(col2[0])
                        nombre_producto.append(col2[1])
                        descripcion_producto.append(col2[2])
                        imagen_producto.append(col2[3])
                        precio_producto.append(col2[4])
                        cantidad_producto.append(col2[5])
                        observaciones_producto.append(col2[6])
                        fecha_creacion_producto.append(col2[8])
                        fecha_actualizacion_producto.append(col2[9])
                        estado_producto.append(col2[10])

                Products = {
                    "id": id_producto,
                    "nombres": nombre_producto,
                    "descripcion": descripcion_producto,
                    "imagen": imagen_producto,
                    "precio": precio_producto,
                    "cantidad": cantidad_producto,
                    "observaciones": observaciones_producto,
                    "fecha_creacion": fecha_creacion_producto,
                    "fecha_actualizacion": fecha_actualizacion_producto
                }
                # endregion
        if logged != True:
            return redirect(url_for('index'))
        else:
            return jsonify(Products), 200

    else:
        return redirect(url_for('index'))


@app.before_request
def limit_remote_addr():
    LISTIPGRNT = ['191.95.144.49', '127.0.0.1', 'localhost']
    if request.remote_addr not in LISTIPGRNT:
        abort(403)  # Forbidden


if __name__ == "__main__":
    app.run(debug=True, host=hostA, port=port)
