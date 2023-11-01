import time

from flask import Flask, render_template, request, redirect, url_for
from DB.ConnectionDB import ConnectionDB
from Model.Program.Program import Program
from Model.Program.Theme import Theme
from Model.Course import Course
import os
import sys
from io import StringIO

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
    def CreateExercise(self=None):
        nameActivity = request.form['nameActivity']
        nameCourse = request.form['CourseName']
        if request.method == "POST":
            nameExercise = request.form["nameExercise"]
            availability = request.form["availability"]
            difficulty = request.form["difficulty"]
            statement = request.form["statement"]

            newExercise = ThemeObject.create_exercise(nameExercise, availability, difficulty, statement)
            ThemeObject.enter_exercise(newExercise, nameActivity, nameCourse)
            listExercisesFromDB = DB.get_exerciseDB(nameActivity, nameCourse)
            ThemeObject.update_exercise(listExercisesFromDB)
            return render_template("HomeMenu_forActivityTeacher.html",
                                   Actividades=ThemeObject.Themes,
                                   Exercises=ThemeObject.Exercises,
                                   CourseName=nameCourse,
                                   nameActivity=nameActivity)

    @app.route("/LoginEmailandPassword", methods=["POST"])
    def LoginE_and_P(self=None):
        if request.method == "POST":
            email = request.form["loginEmail"]
            password = request.form["password"]
            existence, isTeacher = DB.verify_accountDB(email, password)
            if existence and isTeacher:
                return redirect(url_for("SelectCourseView", email=email))
            elif existence:
                CourseName = DB.get_CourseName_by_email_and_password_of_student(email, password)
                ThemeObject.clear_themes()
                ThemeObject.update_themes(CourseName)
                return render_template("HomeMenuStudent.html",
                                       Actividades=ThemeObject.Themes,
                                       CourseName=CourseName)
            else:
                message = "Usuario no existe"
                return render_template("Index.html", message=message)

    @app.route("/SelectCourseView")
    def SelectCourseView(self=None):
        email = request.args.get("email")
        CourseObject.updateList(email)
        return render_template("SelectCourseView.html", Courses=CourseObject.courses, email=email)

    @app.route("/goCourse/<int:Menu>/<string:CourseName>")
    def goCourse(Menu, CourseName):
        ThemeObject.clear_themes()
        ThemeObject.update_themes(CourseName)
        return render_template("HomeMenuTeacher.html",
                               CourseName=CourseName,
                               Actividades=ThemeObject.Themes
                               )

    @app.route("/addCourse/<string:email>", methods=["POST"])
    def addCourse(email):
        course = request.form["todo"]
        CourseObject.courses.append({'task': course})
        CourseObject.enter_course(email, course)
        return redirect(url_for("SelectCourseView", email=email))

    @app.route("/editCourse/<int:Menu>/<string:CourseName>/<string:email>", methods=["GET", "POST"])
    def editCourse(Menu, CourseName, email):
        course = CourseObject.courses[Menu]
        if request.method == "POST":
            course['task'] = request.form['course']
            newCourse = course['task']
            CourseObject.edit_course(CourseName, newCourse)
            CourseObject.updateList(CourseName)
            return redirect(url_for("SelectCourseView", email=email))
        else:
            return render_template("editCourse.html", course=course, Menu=Menu, CourseName=CourseName, email=email)

    @app.route("/deleteCourse/<int:Menu>/<string:CourseName>/<string:email>", methods=["GET","POST"])
    def deleteCourse(Menu, CourseName, email):
        del CourseObject.courses[Menu]
        CourseObject.delete_course(CourseName)
        return redirect(url_for("SelectCourseView", email=email))

    # /----------LISTADO DE ACTIVIDADES------------------------ /

    @app.route("/Menu")
    def Menu(self=None):
        return render_template("HomeMenuTeacher.html",
                               Actividades=Actividades)

    @app.route("/sign_off")
    def sign_off(self=None):
        return render_template("Index.html")

    @app.route("/generateCode")
    def generateCode(message=None):
        CourseName = request.args.get('CourseName')
        idCourse = DB.get_id_course_by_nameDB(CourseName)
        return render_template("HomeMenuTeacher.html",
                               Actividades=ThemeObject.Themes, CourseName=CourseName, idCourse=idCourse)

    @app.route("/add/<string:CourseName>", methods=["POST"])
    def add(CourseName):
        todo = request.form["todo"]
        Actividades.append({"task": todo, "done": False})
        ThemeObject.enter_theme(todo, CourseName)
        return render_template("HomeMenuTeacher.html",
                               Actividades=Actividades, CourseName=CourseName)

    @app.route("/edit/<int:Menu>/<string:actividad>/<string:CourseName>", methods=["GET", "POST"])
    def edit(Menu, actividad, CourseName):
        todo = ThemeObject.Themes[Menu]
        if request.method == "POST":
            todo['task'] = request.form['todo']
            newTheme = todo['task']
            ThemeObject.edit_theme(actividad, newTheme, CourseName)
            return render_template("HomeMenuTeacher.html", Actividades=ThemeObject.Themes, CourseName=CourseName)
        else:
            return render_template("edit.html", todo=todo, Menu=Menu, CourseName=CourseName, actividad=actividad)

    @app.route("/go/<int:Menu>/<string:actividad>/<string:CourseName>")
    def go(Menu, actividad, CourseName):
        listExercisesFromDB = DB.get_exerciseDB(actividad, CourseName)
        ThemeObject.update_exercise(listExercisesFromDB)
        return render_template("HomeMenu_forActivityTeacher.html",
                               Actividades=ThemeObject.Themes,
                               Exercises=ThemeObject.Exercises,
                               nameActivity=actividad,
                               CourseName=CourseName)

    @app.route("/delete/<int:Menu>/<string:CourseName>")
    def delete(Menu, CourseName):
        ThemeObject.delete_theme(ThemeObject.Themes[Menu]['task'], CourseName)
        del ThemeObject.Themes[Menu]
        return render_template("HomeMenuTeacher.html",
                               CourseName=CourseName,
                               Actividades=ThemeObject.Themes)

    @app.route("/editExercise/<int:Menu>/<string:exercise>/<string:CourseName>/<string:nameActivity>",
               methods=["GET", "POST"])
    def editExercise(Menu, exercise, CourseName, nameActivity):
        exercise_ = Exercises[Menu]
        if request.method == "POST":
            exercise_['task'][0] = request.form['nameExercise']
            exercise_['task'][1] = request.form['availability']
            exercise_['task'][2] = request.form['difficulty']
            exercise_['task'][3] = request.form['statement']
            return render_template("HomeMenu_forActivityTeacher.html",
                                   Actividades=Actividades,
                                   Exercises=ThemeObject.Exercises,
                                   CourseName=CourseName,
                                   nameActivity=nameActivity)
        else:
            return render_template("editExercise.html", exercise_=exercise_,
                                   Menu=Menu,
                                   CourseName=CourseName,
                                   exercise=exercise, nameActivity=nameActivity)

    @app.route("/deleteExercise/<int:Menu>/<string:CourseName>/<string:nameActivity>")
    def deleteExercise(Menu, CourseName, nameActivity):
        del Exercises[Menu]
        return render_template("HomeMenu_forActivityTeacher.html",
                               Actividades=Actividades,
                               Exercises=ThemeObject.Exercises,
                               CourseName=CourseName,
                               nameActivity=nameActivity)

    @app.route("/HomeMenuTeacher")
    def Activity(messague=None):
        CourseName = request.args.get('CourseName')
        ThemeObject.update_themes(CourseName)
        return render_template("HomeMenuTeacher.html",
                               CourseName=CourseName,
                               Actividades=ThemeObject.Themes)

    @app.route("/RankingView")  # Segundo Sprint
    def Ranking(message=None):
        CourseName = request.args.get('CourseName')
        # themes = DB.get_themesDB(CourseName)
        themes = Actividades
        ranking_students = {
            "Estudiante 1": 95,
            "Estudiante 2": 87,
            "Estudiante 3": 78,
        }  # se borra cuando este lista la DB
        # ranking_students = DB.update_ranking()
        return render_template("Ranking.html",
                               ranking_students=ranking_students,
                               CourseName=CourseName,
                               Actividades=themes)

    @app.route("/QualifyView")  # Segundo Sprint
    def Qualify(message=None):
        return render_template("Qualify.html")

    # ///////////////////////////////////////////////////////////////////////////////////////#
    # --------------------- METODOS DEL ESTUDIANTE -----------------------------------------#
    @app.route("/HomeMenuStudent")
    def HomeMenuStudent(self=None):
        CourseName = request.args.get('CourseName')
        ThemeObject.update_themes(CourseName)
        return render_template("HomeMenuStudent.html",
                               Actividades=ThemeObject.Themes,
                               CourseName=CourseName)

    @app.route("/StudentRegistrationView")
    def StudentRegistrationView(message=None):
        return render_template("StudentRegistration.html")

    @app.route("/StudentRegistration", methods=["POST"])
    def StudentRegistration(message=None):
        if request.method == "POST":
            nameStudent = request.form["nameStudent"]
            lastNameStudent = request.form["lastNameStudent"]
            emailStudent = request.form["emailStudent"]
            passwordStudent = request.form["passwordStudent"]
            codeCourse = request.form["codeCourse"]
            CourseExists = DB.course_exists_by_code(codeCourse)
            if CourseExists:
                newStudent = program.access.register_student(nameStudent,
                                                             lastNameStudent,
                                                             emailStudent,
                                                             passwordStudent,
                                                             0,
                                                             codeCourse)
                program.access.enter_student(newStudent)
                return redirect(url_for("Index"))
            else:
                messageCourse = "No existe un curso con el codigo que digitaste"
                return render_template("StudentRegistration.html", messageCourse=messageCourse)

    @app.route("/RankingViewStudent")
    def RankingViewStudent(self=None):
        CourseName = request.args.get('CourseName')
        # themes = DB.get_themesDB(CourseName)
        themes = Actividades  # Se borra cuando este lista la DB
        ranking_students = {
            "Estudiante 1": 95,
            "Estudiante 2": 87,
            "Estudiante 3": 78,
        }  # esta se borra cuando este lista la DB
        # ranking_students = DB.update_ranking()
        return render_template("RankingStudent.html",
                               ranking_students=ranking_students,
                               CourseName=CourseName,
                               Actividades=themes)

    @app.route("/DeliveriesStudent")
    def DeliveriesStudent(self=None):  # ejercicios entregados por el estudiante
        pass

    @app.route("/goThemeStudent/<int:Menu>/<string:actividad>/<string:CourseName>")
    def goThemeStudent(Menu, actividad, CourseName):
        listExercisesFromDB = DB.get_exerciseDB(actividad, CourseName)
        ThemeObject.update_exercise(listExercisesFromDB)                     ### cuando ese lista la DB
        ThemeObject.update_themes(CourseName)
        return render_template("HomeMenu_forActivityStudent.html",
                               Actividades=ThemeObject.Themes,
                               Exercises=ThemeObject.Exercises,
                               nameActivity=actividad,
                               CourseName=CourseName)

    @app.route("/goExercise/<int:Menu>/<string:nameExercise>/<string:CourseName>/<string:nameActivity>")
    def goExercise(Menu, nameExercise, CourseName, nameActivity):
        ThemeObject.update_themes(CourseName)
        exerciseObject = DB.get_object_exercise_by_nameExercise_CourseName(nameExercise, CourseName, nameActivity)
        return render_template("ExerciseStudent.html",
                               Actividades=ThemeObject.Themes,
                               exerciseObject=exerciseObject,
                               CourseName=CourseName,
                               nameActivity=nameActivity)

    @app.route("/submitOrExecute")
    def submitOrExecute(self=None):
        code = request.args.get("code")
        exerciseObject = request.args.get("exerciseName")
        nameActivity = request.args.get("nameActivity")
        CourseName = request.args.get("CourseName")
        action = request.args.get("action")
        isEjecutar = action == "Ejecutar"
        if isEjecutar:
            return redirect(url_for("execute", code=code,
                                    exerciseObject=exerciseObject,
                                    nameActivity=nameActivity,
                                    CourseName=CourseName))
        else:
            return redirect(url_for("submitSolution"))

    @app.route("/execute")
    def execute(self=None):
        exerciseObjectInString = request.args.get("exerciseObject")
        exerciseObject = eval(exerciseObjectInString)
        nameActivity = request.args.get("nameActivity")
        CourseName = request.args.get("CourseName")
        code = request.args.get("code")

        # Redirige la salida estándar a un StringIO
        stdout_backup = sys.stdout
        sys.stdout = StringIO()

        # Ejecuta el código proporcionado
        exec(code)

        # Captura la salida estándar
        result = sys.stdout.getvalue()

        # Restaura la salida estándar original
        sys.stdout.close()
        sys.stdout = stdout_backup
        return render_template("ExerciseStudent.html",
                               Actividades=ThemeObject.Themes,
                               exerciseObject=exerciseObject,
                               CourseName=CourseName,
                               nameActivity=nameActivity,
                               compiledCode=result)

    @app.route("/submitExercise")
    def submitExercise(self=None):
        pass
