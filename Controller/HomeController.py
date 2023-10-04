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
            DB.enter_exerciseDB(newExercise, nameActivity, idCourse)
            return render_template("HomeMenu_forActivityTeacher.html",
                                   Actividades=Actividades, Exercises=ThemeObject.Exercises)

    @app.route("/LoginEmailandPassword", methods=["POST"])
    def LoginE_and_P(self=None):
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

    @app.route("/SelectCourseView")
    def SelectCourseView(self=None):
        return render_template("SelectCourseView.html", Courses=Courses)

    @app.route("/goCourse/<int:Menu>/<string:CourseName>")
    def goCourse(Menu, CourseName):
        # listThemesFromDB = DB.get_themesDB(CourseName)
        # ThemeObject.update_themes(listThemesFromDB)
        return render_template("HomeMenuTeacher.html",
                               course_name=CourseName,
                               Actividades=Actividades)

    @app.route("/addCourse", methods=["POST"])
    def addCourse(sell=None):
        course = request.form["todo"]
        Courses.append({'task': course})
        return redirect(url_for("SelectCourseView"))

    @app.route("/editCourse/<int:Menu>", methods=["GET", "POST"])
    def editCourse(Menu):
        course = Courses[Menu]
        if request.method == "POST":
            course['task'] = request.form['course']
            newCourse = course['task']
            DB.edit_courseDB(newCourse)
            CourseObject.enter_course(newCourse)
            return redirect(url_for("SelectCourseView"))
        else:
            return render_template("editCourse.html", course=course, Menu=Menu)

    @app.route("/deleteCourse/<int:Menu>")
    def deleteCourse(Menu):
        nameCourse = Courses[Menu]['task']
        del Courses[Menu]
        DB.delete_courseDB(nameCourse)
        return redirect(url_for("SelectCourseView"))

    # /----------LISTADO DE ACTIVIDADES------------------------ /

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
            ThemeObject.enter_theme(newTheme, 0)
            return redirect(url_for("Menu"))
        else:
            return render_template("edit.html", todo=todo, Menu=Menu)

    @app.route("/go/<int:Menu>/<string:actividad>/<string:nameCourse>")
    def go(Menu, actividad, nameCourse):
        print(actividad)
        listExercisesFromDB = DB.get_exerciseDB(actividad, nameCourse)
        ThemeObject.update_exercise(listExercisesFromDB)
        return render_template("HomeMenu_forActivityTeacher.html",
                               Actividades=Actividades,
                               Exercises=ThemeObject.Exercises,
                               nameActivity=actividad,
                               nameCourse=nameCourse)

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

    @app.route("/RankingView")  # Segundo Sprint
    def Ranking(message=None):
        return render_template("Ranking.html")

    @app.route("/QualifyView")  # Segundo Sprint
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
