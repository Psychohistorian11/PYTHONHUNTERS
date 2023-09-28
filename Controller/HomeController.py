from flask import Flask, render_template, request, redirect, url_for
from DB.ConnectionDB import ConnectionDB
from Model.Program.Program import Program
import os

# creación de objetos
program = Program()
app = Flask(__name__, template_folder=os.path.abspath("templates"),static_folder=os.path.abspath("static"))

class HomeController:

    def __init__(self):
        pass

    def run(self):
        app.run(port=3000, debug=True)

    @app.route("/")
    def Index(message=None):
        return render_template("Index.html", message=message)

    @app.route("/CreateExerciseView")
    def CreateExercise(message=None):
        return render_template("CreateExercise.html")

    @app.route("/LoginEmailandPassword", methods=["POST"])
    def LoginE_and_P(message=None):
        Actividades = [{"todo": "hola", "done": False}]
        if request.method == "POST":
            email = request.form["loginEmail"]
            password = request.form["password"]
            existence, isTeacher = ConnectionDB.verify_accountDB(email, password)
            if existence and isTeacher:
                return render_template("HomeMenuTeacher.html",Actividades=Actividades)
            elif existence:
                return render_template("HomeMenuStudent.html")
            else:
                message = "Usuario no existe"
                return redirect(url_for("Index", message=message))

    @app.route("/StudentRegistrationView")
    def StudentRegistrationView(message=None):
        return render_template("StudentRegistration.html")

    @app.route("/RankingView")
    def Ranking(message=None):
        return render_template("Ranking.html")

    @app.route("/QualifyView")
    def Qualify(message=None):
        return render_template("Qualify.html")
    @app.route("/StudentRegistration", methods=["POST"])
    def StudentRegistration(message=None):
        if request.method == "POST":
            nameStudent = request.form["nameStudent"]
            lastNameStudent = request.form["lastNameStudent"]
            emailStudent = request.form["emailStudent"]
            passwordStudent = request.form["emailStudent"]

            # Creación e IngresoDB
            newStudent = program.access.register_student(nameStudent, lastNameStudent, emailStudent, passwordStudent, 0)
            program.access.enter_student(newStudent)
