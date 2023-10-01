from flask import Flask, render_template, request, redirect, url_for
from DB.ConnectionDB import ConnectionDB
from Model.Program.Program import Program
from Model.Program.Theme import Theme
import os

# creación de objetos
program = Program()
app = Flask(__name__, template_folder=os.path.abspath("templates"), static_folder=os.path.abspath("static"))
DB = ConnectionDB
Actividades = Theme().Themes
Exercise = 0


class HomeController:

    def __init__(self):
        pass

    def run(self):
        app.run(port=3000, debug=True)

    @app.route("/")
    def Index(message=None):
        return render_template("Index.html", message=message)

    @app.route("/CreateExerciseView")
    def CreateExerciseView(message=None):
        return render_template("CreateExercise.html")

    @app.route("/CreateExercise", methods=["POST"])
    def CreateExcercise(messague=None):
        if request.method == "POST":
            nameExercise = request.form["nameExercise"]
            availability = request.form["availability"]
            difficulty = request.form["difficulty"]
            statement = request.form["statement"]
            newExercise = Theme().create_exercise(nameExercise, availability, difficulty, statement)
            ConnectionDB().enter_ExerciseDB(newExercise)


    @app.route("/LoginEmailandPassword", methods=["POST"])
    def LoginE_and_P(messague1=None):

        if request.method == "POST":
            email = request.form["loginEmail"]
            password = request.form["password"]
            existence, isTeacher = ConnectionDB().verify_accountDB(email, password)
            if existence and isTeacher:
                return redirect(url_for("Menu"))
            elif existence:
                return render_template("HomeMenuStudent.html")
            else:
                message = "Usuario no existe"
                return redirect(url_for("Index", message=message))

    # /----------LISTADO DE ACTIVIDADES------------------------
    @app.route("/Menu")
    def Menu(messague=None):
        return render_template("HomeMenuTeacher.html", Actividades=Actividades)

    @app.route("/add", methods=["POST"])
    def add(messague=None):
        todo = request.form["todo"]
        Actividades.append({"task": todo, "done": False})
        return redirect(url_for("Menu"))

    @app.route("/edit/<int:Menu>", methods=["GET", "POST"])
    def edit(Menu):
        todo = Actividades[Menu]
        if request.method == "POST":
            todo['task'] = request.form['todo']
            newTheme = todo['task']
            Theme().enter_Theme(newTheme)
            return redirect(url_for("Menu"))
        else:
            return render_template("edit.html", todo=todo, Menu=Menu)

    @app.route("/go/<int:Menu>")
    def go(Menu):
        return render_template("HomeMenu_forActivityTeacher.html", Exercise=Exercise)

    @app.route("/check/<int:Menu>")  # Metodo no Utilizado
    def check(Menu):
        Actividades[Menu]['done'] = not Actividades[Menu]['done']
        return redirect(url_for("Menu"))

    @app.route("/delete/<int:Menu>")
    def delete(Menu):
        del Actividades[Menu]
        return redirect(url_for("Menu"))

    # *--------------------------------------------------------------------------

    @app.route("/StudentRegistrationView")
    def StudentRegistrationView(message=None):
        return render_template("StudentRegistration.html")

    @app.route("/HomeMenuTeacher")
    def Activity(messague=None):
        return render_template("HomeMenuTeacher.html")

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
