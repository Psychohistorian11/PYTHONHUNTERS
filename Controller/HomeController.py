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
        CourseName = request.args.get('CourseName')
        return render_template("CreateExercise.html",
                               Actividades=Actividades,
                               nameActivity=nameActivity,
                               CourseName=CourseName)

    @app.route("/CreateExercise", methods=["POST"])
    def CreateExcercise(self=None):
        nameActivity = request.form['nameActivity']
        nameCourse = request.form['CourseName']
        if request.method == "POST":
            nameExercise = request.form["nameExercise"]
            availability = request.form["availability"]
            difficulty = request.form["difficulty"]
            statement = request.form["statement"]
    
            newExercise = ThemeObject.create_exercise(nameExercise, availability, difficulty, statement)
            ThemeObject.update_exercise(newExercise)
            #DB.enter_exerciseDB(newExercise, nameActivity, nameCourse)
            #listExercisesFromDB = DB.get_exerciseDB(nameActivity, nameCourse)
            #ThemeObject.update_exercise(listExercisesFromDB)
            return render_template("HomeMenu_forActivityTeacher.html",
                                       Actividades=Actividades,
                                   Exercises=ThemeObject.Exercises,
                                   CourseName=nameCourse,
                                   nameActivity=nameActivity)

    @app.route("/LoginEmailandPassword", methods=["POST"])
    def LoginE_and_P(self=None):
        if request.method == "POST":
            email = request.form["loginEmail"]
            password = request.form["password"]
            existence, isTeacher = ConnectionDB().verify_accountDB(email, password)
            if existence and isTeacher:
                return redirect(url_for("SelectCourseView"))
            elif existence:
                return render_template("HomeMenuStudent.html",Actividades=Actividades)
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
                               CourseName=CourseName,
                               Actividades=Actividades
                               )

    @app.route("/addCourse", methods=["POST"])
    def addCourse(sell=None):
        course = request.form["todo"]
        Courses.append({'task': course})
        CourseObject.enter_course(course)
        return redirect(url_for("SelectCourseView"))

    @app.route("/editCourse/<int:Menu>/<string:CourseName>", methods=["GET", "POST"])
    def editCourse(Menu, CourseName):
        course = Courses[Menu]
        if request.method == "POST":
            course['task'] = request.form['course']
            newCourse = course['task']
            CourseObject.edit_course(CourseName, newCourse)
            return redirect(url_for("SelectCourseView"))
        else:
            return render_template("editCourse.html", course=course, Menu=Menu,CourseName=CourseName)

    @app.route("/deleteCourse/<int:Menu>")
    def deleteCourse(Menu):
        nameCourse = Courses[Menu]['task']
        del Courses[Menu]
        CourseObject.delete_course(nameCourse)
        return redirect(url_for("SelectCourseView"))

    # /----------LISTADO DE ACTIVIDADES------------------------ /

    @app.route("/Menu")
    def Menu(self=None):
        return render_template("HomeMenuTeacher.html",
                               Actividades=Actividades)

    @app.route("/sign_off")
    def sign_off(self=None):
        return render_template("Index.html")

    @app.route("/add/<string:CourseName>", methods=["POST"])
    def add(CourseName):
        todo = request.form["todo"]
        Actividades.append({"task": todo, "done": False})
        print(f"add: {Actividades}")
        #ThemeObject.enter_theme(odo CourseName)
        return render_template("HomeMenuTeacher.html",
                               Actividades=Actividades, CourseName=CourseName)

    @app.route("/edit/<int:Menu>/<string:actividad>/<string:CourseName>", methods=["GET", "POST"])
    def edit(Menu, actividad, CourseName):
        print(f"edit: {Actividades}")
        todo = Actividades[Menu]
        if request.method == "POST":
            todo['task'] = request.form['todo']
            newTheme = todo['task']
            #ThemeObject.edit_theme(newTheme, actividad, CourseName)
            return render_template("HomeMenuTeacher.html", Actividades=Actividades, CourseName=CourseName)
        else:
            return render_template("edit.html", todo=todo, Menu=Menu, CourseName=CourseName, actividad=actividad)

    @app.route("/go/<int:Menu>/<string:actividad>/<string:CourseName>")
    def go(Menu, actividad, CourseName):
        print(CourseName)
        #listExercisesFromDB = DB.get_exerciseDB(actividad, nameCourse)
        #ThemeObject.update_exercise(listExercisesFromDB)
        return render_template("HomeMenu_forActivityTeacher.html",
                               Actividades=Actividades,
                               Exercises=ThemeObject.Exercises,
                               nameActivity=actividad,
                               CourseName=CourseName)

    @app.route("/check/<int:Menu>")  # Metodo no Utilizado
    def check(Menu):
        Actividades[Menu]['done'] = not Actividades[Menu]['done']
        return redirect(url_for("Menu"))

    @app.route("/delete/<int:Menu>/<string:CourseName>")
    def delete(Menu,CourseName):
        #nameTheme = Actividades[Menu]['task']
        del Actividades[Menu]
        #ThemeObject.delete_theme(nameTheme, CourseName)
        return render_template("HomeMenuTeacher.html",
                               CourseName=CourseName,
                               Actividades=Actividades)

    @app.route("/StudentRegistrationView")
    def StudentRegistrationView(message=None):
        return render_template("StudentRegistration.html")

    @app.route("/HomeMenuTeacher")
    def Activity(messague=None):
        CourseName = request.args.get('CourseName')
        return render_template("HomeMenuTeacher.html",
                               CourseName=CourseName,
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
            passwordStudent = request.form["passwordStudent"]

            # Creación e IngresoDB
            newStudent = program.access.register_student(nameStudent,
                                                         lastNameStudent,
                                                         emailStudent,
                                                         passwordStudent, 0)
            program.access.enter_student(newStudent)
            return redirect(url_for("Index"))
