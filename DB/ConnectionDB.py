from typing import Tuple

from flask_mysqldb import MySQL
from flask import Flask
import os

app = Flask(__name__, template_folder=os.path.abspath("templates"))

mysql = MySQL()
app.config['MYSQL_HOST'] = 'db4free.net'
app.config['MYSQL_USER'] = 'bit_busters'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'pythonbd'
mysql.init_app(app)


class ConnectionDB:

    def __init__(self, app):
        self.app = app
        mysql.init_app(app)

    def verify_accountDB(self, email, password) -> tuple[bool, bool]:
        existence: bool = True
        isTeacher = True
        cur = mysql.connection.cursor()
        cur.execute()  # dentro de ese parentesis irá la consulta a la base de datos
        mysql.connection.commit()  # Ejecutamos la consulta
        return existence, isTeacher

    def Enter_studentDB(self, newStudent):  # Ingresar nuevo estudiante a la  base de datos
        pass
