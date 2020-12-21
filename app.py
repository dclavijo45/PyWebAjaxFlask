from flask import Flask, request, jsonify, render_template, session

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


@app.route("/usuarios", methods=["POST", "GET"])
def usuarios():
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
                jsonfy = {"status": 200, "msg": "Login success", "Logged": True}
                logged = True
                session["id"] = id
                break
        if logged != True:
            jsonfy = {
                "status": 499,
                "msg": "Login failed, user or pwd error",
                "Logged": False,
            }
    else:
        jsonfy = {"status": 499, "msg": "Access only for method POST", "Logged": False}
    return jsonify(jsonfy), 200


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="localhost")
