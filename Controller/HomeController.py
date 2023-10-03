from flask import Flask, render_template, request, redirect, url_for
from DB.ConnectionDB import ConnectionDB
from Model.Program.Program import Program
from Model.Program.Theme import Theme
from Model.Course import Course
import os

# creación de objetos
program = Program()  # program controla toda la logica del modelo
ThemeObject = Theme()  # Simplemente contiene la información de los temas
CourseObject = Course()
app = Flask(__name__, template_folder=os.path.abspath("templates"),
            static_folder=os.path.abspath("static"))
DB = ConnectionDB()  # DB controla la información que llega y sale de la base de datos al controlador
Courses = CourseObject.courses
Actividades = ThemeObject.Themes
Exercises = ThemeObject.Exercises


class HomeController:

    def __init__(self):
        pass

    def run(self):
        app.run(port=3000, debug=True)

    @app.route("/")
    def Index(message=None):
        return render_template("Index.html", message=message)

    @app.route("/CreateExerciseView")
    def CreateExerciseView(self=None):
        nameActivity = request.args.get('nameActivity')
        return render_template("CreateExercise.html",
                               Actividades=Actividades,
                               nameActivity=nameActivity)

    @app.route("/CreateExercise", methods=["POST"])
    def CreateExcercise(self=None):
        idCourse = 0
        nameActivity = request.args.get('nameActivity')
        listExercisesFromDB = DB.get_exerciseDB(nameActivity, idCourse)
        ThemeObject.update_exercise(listExercisesFromDB)
        if request.method == "POST":
            nameExercise = request.form["nameExercise"]
            availability = request.form["availability"]
            difficulty = request.form["difficulty"]
            statement = request.form["statement"]

            newExercise = ThemeObject.create_exercise(nameExercise, availability, difficulty, statement)
            DB.enter_exerciseDB(newExercise, nameActivity)
            return render_template("HomeMenu_forActivityTeacher.html",
                                   Actividades=Actividades, Exercises=ThemeObject.Exercises)

    @app.route("/LoginEmailandPassword", methods=["POST"])
    def LoginE_and_P(self=None):
        edd =0 
        listThemesFromDB = DB.get_themesDB(edd)
        idCourse = 0
        listThemesFromDB = DB.get_themesDB(idCourse)
        ThemeObject.update_themes(listThemesFromDB)
        if request.method == "POST":
            email = request.form["loginEmail"]
            password = request.form["password"]
            existence, isTeacher = ConnectionDB().verify_accountDB(email, password)
            if existence and isTeacher:
                return redirect(url_for("SelectCourseView"))
            elif existence:
                return render_template("HomeMenuStudent.html")
            else:
                message = "Usuario no existe"
                return render_template("Index.html", message=message)

    # /----------LISTADO DE ACTIVIDADES------------------------ /
    @app.route("/SelectCourseView")
    def SelectCourseView(self=None):
        return render_template("SelectCourseView.html", Courses=Courses)
    @app.route("/Menu")
    def Menu(self=None):
        return render_template("HomeMenuTeacher.html",
                               Actividades=Actividades)

    @app.route("/sign_off")
    def sign_off(self=None):
        return render_template("Index.html")

    @app.route("/add", methods=["POST"])
    def add(self=None):
        todo = request.form["todo"]
        Actividades.append({"task": todo, "done": False})
        return redirect(url_for("Menu"))

    @app.route("/edit/<int:Menu>", methods=["GET", "POST"])
    def edit(Menu):
        todo = Actividades[Menu]
        if request.method == "POST":
            todo['task'] = request.form['todo']
            newTheme = todo['task']
            idCourse = 0
            ThemeObject.enter_theme(newTheme,idCourse)
            return redirect(url_for("Menu"))
        else:
            return render_template("edit.html", todo=todo, Menu=Menu)

    @app.route("/go/<int:Menu>/<string:actividad>")
    def go(Menu, actividad):
        idCourse= 0
        listExercisesFromDB = DB.get_exerciseDB(actividad,idCourse)
        ThemeObject.update_exercise(listExercisesFromDB)
        return render_template("HomeMenu_forActivityTeacher.html",
                               Actividades=Actividades,
                               Exercises=ThemeObject.Exercises,
                               nameActivity=actividad)

    @app.route("/check/<int:Menu>")  # Metodo no Utilizado
    def check(Menu):
        Actividades[Menu]['done'] = not Actividades[Menu]['done']
        return redirect(url_for("Menu"))

    @app.route("/delete/<int:Menu>")
    def delete(Menu):
        del Actividades[Menu]
        return redirect(url_for("Menu"))


    @app.route("/StudentRegistrationView")
    def StudentRegistrationView(message=None):
        return render_template("StudentRegistration.html")

    @app.route("/HomeMenuTeacher")
    def Activity(messague=None):
        return render_template("HomeMenuTeacher.html",
                               Actividades=Actividades)

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
            newStudent = program.access.register_student(nameStudent,
                                                         lastNameStudent,
                                                         emailStudent,
                                                         passwordStudent, 0)
            program.access.enter_student(newStudent)
            return redirect(url_for("Index"))
