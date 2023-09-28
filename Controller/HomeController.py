from flask import Flask, render_template, request, redirect, url_for
from DB.ConnectionDB import ConnectionDB
from Model.Program.Program import Program
import os

# creación de objetos
program = Program()
app = Flask(__name__, template_folder=os.path.abspath("templates"))


class HomeController:

    def __init__(self):
        pass

    def run(self):
        app.run(port=3000, debug=True)

    @app.route("/")
    def Index():
        return render_template("Index.html")

    @app.route("/LoginEmailandPassword", methods=["POST"])
    def LoginE_and_P():
        if request.method == "POST":
            email = request.form["loginEmail"]
            password = request.form["password"]
            # ConnectionDB.verify_accountDB(email, password)

            return redirect(url_for("Index"))

    @app.route("/StudentRegistrationView")
    def StudentRegistrationView():
        return render_template("StudentRegistration.html")

    @app.route("/StudentRegistration", methods=["POST"])
    def StudentRegistration():
        if request.method == "POST":
            nameStudent = request.form["nameStudent"]
            lastNameStudent = request.form["lastNameStudent"]
            emailStudent = request.form["emailStudent"]
            passwordStudent = request.form["emailStudent"]

            # Creación e IngresoDB
            newStudent = program.access.register_student(nameStudent, lastNameStudent, emailStudent, passwordStudent, 0)
            program.access.enter_student(newStudent)
