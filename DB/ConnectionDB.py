import mysql.connector

from Model.Delivery import Delivery
from Model.Program.Exercise import Exercise
from Model.Student import Student


config = {'user': 'root',
          'host': 'localhost',
          'password': 'Palabrasambiguas',
          'database': 'pythonbd',
          'port': 3306,  # Puerto predeterminado de MySQL
          'raise_on_warnings': True}  # Para que se generen excepciones en caso de advertencias


class ConnectionDB:
    conn = None  # Mantén la conexión abierta en la instancia

    def init(self):
        pass

    def executeSQL(self, consulta_sql, variables_adicionales=None):
        try:
            conn = mysql.connector.connect(**config)  # Abre la conexión si no está abierta

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(consulta_sql, variables_adicionales)

                if consulta_sql.strip().upper().startswith("INSERT") or consulta_sql.strip().upper().startswith(
                        "UPDATE") or consulta_sql.strip().upper().startswith(
                    "DELETE") or consulta_sql.strip().upper().startswith("CREATE"):
                    conn.commit()
                    return None

                resultados = cursor.fetchall()
                conn.close()
                return resultados
        except mysql.connector.Error as e:
            print("Error al conectar a la base de datos:", e)

    def verify_accountDB(self, email, password) -> tuple[bool, bool]:
        teacher_query = 'select count(*) from Profesor where correo = %s and contrasenia = %s'
        teacher_results = self.executeSQL(teacher_query, (email, password))
        quantity_teacher = 0
        if teacher_results is not None:
            quantity_teacher = teacher_results[0][0]
        existence_teacher = quantity_teacher >= 1
        existence_student = False
        if not existence_teacher:
            student_query = 'select count(*) from Estudiante where correo = %s and contrasenia = %s'
            student_results = self.executeSQL(student_query, (email, password))
            quantity_student = student_results[0][0]

            existence_student = quantity_student >= 1

        existence = False
        if existence_teacher or existence_student:
            existence = True
        return existence, existence_teacher

    def enter_studentDB(self, newStudent):  # Ingresar nuevo estudiante a la  base de datos, no retorna nada
        query = """INSERT INTO Estudiante
        (`idEstudiante`,
        `curso_idCurso`,
        `nombre`,
        `apellido`,
        `correo`,
        `contrasenia`,
        `puntaje`)
        VALUES
        (null,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s);
        """
        if newStudent.score != 0:
            if newStudent.score is None:
                newStudent.score = 0
        variables = (newStudent.codeCourse, newStudent.firstName, newStudent.lastName,
                     newStudent.email, newStudent.password, newStudent.score)
        self.executeSQL(query, variables)

    def exist_themeDB(self, newTheme, nameCourse):
        idTheme = self.get_id_course_by_nameDB(nameCourse)
        query = """SELECT COUNT(*) FROM Tematica WHERE curso_idCurso = %s AND nombre = %s;"""
        variables = (idTheme, newTheme)
        result = self.executeSQL(query, variables)
        exist = True
        if result:
            exist = result[0][0] >= 1
        return exist

    def enter_ThemeDB(self, newTheme, nameCourse):  # Ingresar nuevo tema a la base de datos, no retorna nada
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        query = """INSERT INTO Tematica
                    VALUES
                    (null,%s,%s);
                    """
        self.executeSQL(query, (idCourse, newTheme))

    def edit_themeDB(self, actualName, newThemeName, nameCourse):
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(actualName, idCourse)
        query = """UPDATE Tematica SET nombre = %s WHERE (idTematica = %s) and (curso_idCurso = %s);"""
        variables = (newThemeName, idTheme, idCourse)
        self.executeSQL(query, variables)

    def delete_themeDB(self, theme, nameCourse):
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(theme, idCourse)

        query = """DELETE FROM Tematica
        WHERE `idTematica` = %s AND `curso_idCurso` = %s;"""
        variables = (idTheme, idCourse)
        self.executeSQL(query, variables)

    def get_themesDB(self, nameCourse):  # Este metodo me entrega todos los temas que se
        # encuentran en la base de datos, necesito solo los nombres
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        # print("este es el idCourse:",idCourse)
        query = """select t.nombre from Tematica t
                  where t.curso_idCurso = %s ;"""
        result = self.executeSQL(query, (idCourse,))
        themes = [name[0] for name in result]
        # print("lista de temas de db: ", themes)
        return themes

    def get_id_theme_by_nameDB(self, nameTheme, idCourse):
        query_by_id_theme = """SELECT idTematica from Tematica t where t.nombre = %s AND t.curso_idCurso = %s;"""
        variables = (nameTheme, idCourse)
        listidTheme = self.executeSQL(query_by_id_theme, variables)
        idTheme = 0
        if listidTheme:
            idTheme = listidTheme[0][0]
        return idTheme

    def get_id_course_by_nameDB(self, nameCourse):
        query_by_id_course = """SELECT idCurso from Curso c where nombre = %s"""
        listidCourse = self.executeSQL(query_by_id_course, (nameCourse,))
        idCourse = 0
        if listidCourse:
            idCourse = listidCourse[0][0]
        return idCourse

    def exist_exerciseDB(self, newExercise: Exercise, nameTheme, nameCourse):
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme, idCourse)
        query = """SELECT COUNT(*) FROM Ejercicio WHERE tematica_curso_idCurso = %s 
        AND tematica_idTematica = %s AND nombre = %s;"""
        variables = (idCourse, idTheme, newExercise.nameExercise)
        result = self.executeSQL(query, variables)
        exist = True
        if result:
            exist = result[0][0] >= 1
        return exist

    def enter_exerciseDB(self, newExercise, nameTheme, nameCourse):
        print("esto:", newExercise.availability)
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme, idCourse)
        query = """INSERT INTO Ejercicio VALUES (null,%s,%s,%s,%s,%s,%s);"""
        available = 0
        if newExercise.availability == "1":
            available = 1
        variables = (idTheme, idCourse, newExercise.nameExercise,
                     newExercise.statement, available, newExercise.difficulty)
        self.executeSQL(query, variables)

    def get_exerciseDB(self, nameTheme, nameCourse):  # Este metodo lo puede usar sólo el profesor
        # ser autoincremento y el valor es una lista con los atributos del Ejercicio
        # El parametro IDnameTheme es la clave foranea de la tabla ejercicio para encontrar
        # los ejercicios correspondientes a una actividad
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme, idCourse)
        query = """SELECT e.idEjercicio,e.nombre,e.disponibilidad,e.dificultad,e.enunciado FROM Ejercicio e 
        JOIN Tematica t ON e.tematica_idTematica = t.idTematica WHERE t.idTematica
        = %s and t.curso_idCurso = %s;"""
        lista_resultados = self.executeSQL(query, (idTheme, idCourse))
        lista_ejercicio = []
        valor = False
        for ejercicio in lista_resultados:
            if ejercicio[2] == 1:
                valor = True
            e = Exercise(ejercicio[1], valor, ejercicio[3], ejercicio[4])
            lista_ejercicio.append(e)
        return lista_ejercicio

    def get_exercise_studentDB(self, nameTheme,
                               nameCourse):  # Este metodo me entrega un diccionario donde la clave puede
        # ser autoincremento y el valor es una lista con los atributos del Ejercicio
        # El parametro IDnameTheme es la clave foranea de la tabla ejercicio para encontrar
        # los ejercicios correspondientes a una actividad
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme, idCourse)
        query = """SELECT e.idEjercicio,e.nombre,e.disponibilidad,e.dificultad,e.enunciado FROM Ejercicio e 
        JOIN Tematica t ON e.tematica_idTematica = t.idTematica WHERE t.idTematica
        = %s and t.curso_idCurso = %s and e.disponibilidad = 1;"""
        lista_resultados = self.executeSQL(query, (idTheme, idCourse))
        lista_ejercicio = []
        valor = False
        for ejercicio in lista_resultados:
            if ejercicio[2] == 1:
                valor = True
            e = Exercise(ejercicio[1], valor, ejercicio[3], ejercicio[4])
            lista_ejercicio.append(e)
        return lista_ejercicio

    def edit_exerciseDB(self, newExercise, oldNameExercise, nameTheme, nameCourse):
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme, idCourse)
        idExercise = self.get_id_exercise_by_nameDB(oldNameExercise, idTheme, idCourse)
        query = """UPDATE Ejercicio SET nombre = %s, 
        enunciado = %s, disponibilidad = %s, dificultad = %s
        WHERE idEjercicio = %s AND tematica_idTematica = %s 
        AND tematica_curso_idCurso = %s;"""
        available = 0
        if newExercise.availability:
            available = 1
        variables = (newExercise.nameExercise, newExercise.statement,
                     available, newExercise.difficulty,
                     idExercise, idTheme, idCourse)
        self.executeSQL(query, variables)

    def delete_exerciseDB(self, nameExercise, nameTheme, nameCourse):
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme, idCourse)
        idExercise = self.get_id_exercise_by_nameDB(nameExercise, idTheme, idCourse)
        query = """DELETE FROM Ejercicio
        WHERE idEjercicio = %s AND tematica_idTematica = %s AND tematica_curso_idCurso = %s;"""
        variables = (idExercise, idTheme, idCourse)
        self.executeSQL(query, variables)

    def get_id_teacher_by_emailDB(self, teacherEmail):
        query = """SELECT idProfesor from Profesor where correo = %s"""
        listidTeacher = self.executeSQL(query, (teacherEmail,))
        idTeacher = 0
        if listidTeacher:
            idTeacher = listidTeacher[0][0]
        return idTeacher

    def exist_courseDB(self, nameCourse):
        query = """SELECT COUNT(*) FROM Curso WHERE nombre = %s;"""
        variables = (nameCourse,)
        result = self.executeSQL(query, variables)
        exist = True
        if result:
            exist = result[0][0] >= 1
        return exist

    def enter_courseDB(self, teacherEmail, nameCourse):
        idTeacher = self.get_id_teacher_by_emailDB(teacherEmail)
        query = """insert into Curso values (null,%s,%s)"""
        self.executeSQL(query, (idTeacher, nameCourse))

    def delete_courseDB(self, nameCourse):
        query = """delete from Curso where nombre = %s"""
        self.executeSQL(query, (nameCourse,))

    def edit_courseDB(self, actualCourse, newCourseName):
        idCourse = self.get_id_course_by_nameDB(actualCourse)
        query = """UPDATE Curso SET nombre = %s WHERE (idCurso = %s);"""
        variables = (newCourseName, idCourse)
        self.executeSQL(query, variables)

    def get_coursesDB(self, emailTeacher):
        idTeacher = self.get_id_teacher_by_emailDB(emailTeacher)
        query = """select c.nombre from Curso c
                  where c.profesor_idProfesor = %s ;"""
        result = self.executeSQL(query, (idTeacher,))
        courses = []
        if result:
            courses = [name[0] for name in result]
        return courses

    def update_ranking(self, courseName):
        idCourse = self.get_id_course_by_nameDB(courseName)
        ranking_students = {
            "Estudiante 1": 95,
            "Estudiante 2": 87,
            "Estudiante 3": 78,
        }
        dic = {}
        query = """SELECT nombre, puntaje FROM Estudiante 
        WHERE curso_idCurso = %s ORDER BY puntaje DESC LIMIT 5"""
        variables = (idCourse,)
        result = self.executeSQL(query, variables)
        for fila in result:
            nombre = fila[0]
            puntaje = fila[1]
            dic[nombre] = puntaje
        return dic

    def course_exists_by_code(self, idCourse):
        query = """SELECT COUNT(*) FROM Curso where idCurso = %s;"""
        results = self.executeSQL(query, (idCourse,))
        quantity = 0
        if results is not None:
            quantity = results[0][0]
        exist = quantity >= 1
        return exist

    def get_CourseName_by_email_and_password_of_student(self, email, password):
        teacher_query = """SELECT c.nombre FROM Estudiante e JOIN Curso c ON e.curso_idCurso = c.idCurso 
        WHERE e.correo = %s AND e.contrasenia = %s;"""
        variables = (email, password)
        results = self.executeSQL(teacher_query, variables)
        CourseName = ""
        if results:
            CourseName = results[0][0]
        return CourseName

    # En realidad retorna una lista con la info del ejercicio
    def get_object_exercise_by_nameExercise_CourseName(self, nameExercise, courseName, themeName):
        idCourse = self.get_id_course_by_nameDB(courseName)
        idTheme = self.get_id_theme_by_nameDB(themeName, idCourse)
        query = """SELECT * FROM Ejercicio WHERE nombre = %s
                AND tematica_curso_idCurso = %s AND tematica_idTematica = %s;"""
        variables = (nameExercise, idCourse, idTheme)
        result = self.executeSQL(query, variables)
        primera_fila = result[0]
        available = False
        if primera_fila[5] == 1:
            available = True
        exercise = [primera_fila[3], available,
                    primera_fila[6], primera_fila[4]]
        return exercise

    def get_id_exercise_by_nameDB(self, exerciseName, idTheme, idCourse):
        query = """SELECT idEjercicio from Ejercicio e where nombre = %s and
         tematica_idTematica = %s and tematica_curso_idCurso=%s;"""
        variables = (exerciseName, idTheme, idCourse)
        result = self.executeSQL(query, variables)
        idExercise = 0
        if result:
            idExercise = result[0][0]
        return idExercise

    def get_id_student_by_emailDB(self, emailStudent):
        query = """SELECT idEstudiante from Estudiante e where correo = %s"""
        listidStudent = self.executeSQL(query, (emailStudent,))
        idStudent = 0
        if listidStudent:
            idStudent = listidStudent[0][0]
        return idStudent

    def submit_exercise(self, nameExercise, emailStudent, nameTheme, nameCourse, code, detail):
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme, idCourse)
        idExercise = self.get_id_exercise_by_nameDB(nameExercise, idTheme, idCourse)
        idStudent = self.get_id_student_by_emailDB(emailStudent)
        variables = (idStudent, idExercise, idTheme, idCourse, code, detail)
        # print("mail: ", emailStudent)
        # print("idStudent: ",idStudent)
        # print("code: ", code)
        # print("detail: ", detail)
        query = """INSERT INTO Entrega VALUES
        (null,%s,%s,%s,%s,%s,%s,null,null);"""
        if detail == "":
            # No le mando detalle, sino null
            variables = (idStudent, idExercise, idTheme, idCourse, code)
            query = """INSERT INTO Entrega VALUES
            (null,%s,%s,%s,%s,%s,null,null,null);"""

        self.executeSQL(query, variables)

    def get_student_and_deliveryDB(self, exercise, CourseName, nameActivity):
        idCourse = self.get_id_course_by_nameDB(CourseName)
        idTheme = self.get_id_theme_by_nameDB(nameActivity, idCourse)
        idExercise = self.get_id_exercise_by_nameDB(exercise, idTheme, idCourse)
        query = """SELECT e.nombre, e.apellido, e.correo, e.contrasenia,
        e.puntaje, e.curso_idCurso,
        ej.nombre, en.respuesta, en.detalles, en.retroalimentacion, en.nota
        FROM Estudiante e JOIN Entrega en 
        ON e.idEstudiante = en.estudiante_idEstudiante
        JOIN Ejercicio ej 
        ON ej.idEjercicio = en.ejercicio_idEjercicio
        WHERE en.ejercicio_tematica_curso_idCurso = %s
        AND en.ejercicio_tematica_idTematica = %s
        AND en.ejercicio_idEjercicio = %s;"""
        variables = (idCourse, idTheme, idExercise)
        result = self.executeSQL(query, variables)
        list_def = []
        for row in result:
            detail = ""
            if row[8] is not None:
                detail = row[8]
            feedback = ""
            if row[9] is not None:
                feedback = row[9]
            note = ""
            if row[10] is not None:
                note = row[10]
            NewStudent = Student(row[0], row[1], row[2], row[3], row[4], row[5])
            NewDelivery = Delivery(row[6], row[7], detail, feedback, note)
            list_def.append([NewStudent, NewDelivery])
        return list_def

    def deliverNoteDB(self, nameActivity, nameExercise, CourseName, email,
                      detail, code, note, feedback):
        idCourse = self.get_id_course_by_nameDB(CourseName)
        idTheme = self.get_id_theme_by_nameDB(nameActivity, idCourse)
        idExercise = self.get_id_exercise_by_nameDB(nameExercise, idTheme, idCourse)
        idStudent = self.get_id_student_by_emailDB(email)
        query = """UPDATE Entrega SET
        `respuesta` = %s, `detalles` = %s,
        `retroalimentacion` = %s, `nota` = %s
        WHERE `estudiante_idEstudiante` = %s  
        AND `ejercicio_idEjercicio` = %s
        AND `ejercicio_tematica_idTematica` = %s 
        AND `ejercicio_tematica_curso_idCurso` = %s;"""
        if detail == "":
            detail = None
        variables = (code, detail, feedback, note,
                     idStudent, idExercise, idTheme, idCourse)
        self.executeSQL(query, variables)
        # Actualizar puntaje estudiante
        query = """UPDATE Estudiante SET
        `puntaje` = `puntaje` + %s
        WHERE `idEstudiante` = %s AND `curso_idCurso` = %s;"""
        variables = (note, idStudent, idCourse)
        self.executeSQL(query, variables)

    def exerciseDeliveredDB(self, nameExercise, CourseName, nameActivity, email):
        idStudent = self.get_id_student_by_emailDB(email)
        idCourse = self.get_id_course_by_nameDB(CourseName)
        idTheme = self.get_id_theme_by_nameDB(nameActivity, idCourse)
        idExercise = self.get_id_exercise_by_nameDB(nameExercise, idTheme, idCourse)
        query = """SELECT COUNT(*) FROM Entrega
        WHERE `estudiante_idEstudiante` = %s
        AND `ejercicio_idEjercicio` = %s
        AND `ejercicio_tematica_idTematica` = %s
        AND `ejercicio_tematica_curso_idCurso` = %s;"""
        variables = (idStudent, idExercise, idTheme, idCourse)
        result = self.executeSQL(query, variables)
        quantity = 0
        if result is not None:
            quantity = result[0][0]
        exist = quantity >= 1
        return exist

    def get_deliver_studentDB(self, email, CourseName, nameActivity, exercise):
        idStudent = self.get_id_student_by_emailDB(email)
        idCourse = self.get_id_course_by_nameDB(CourseName)
        idTheme = self.get_id_theme_by_nameDB(nameActivity, idCourse)
        idExercise = self.get_id_exercise_by_nameDB(exercise, idTheme, idCourse)
        query = """SELECT e.nombre, e.apellido, e.correo, e.contrasenia,
        e.puntaje, e.curso_idCurso,
        ej.nombre, en.respuesta, en.detalles, en.retroalimentacion, en.nota
        FROM Estudiante e JOIN Entrega en 
        ON e.idEstudiante = en.estudiante_idEstudiante
        JOIN Ejercicio ej 
        ON ej.idEjercicio = en.ejercicio_idEjercicio
        WHERE en.ejercicio_tematica_curso_idCurso = %s
        AND en.ejercicio_tematica_idTematica = %s
        AND en.ejercicio_idEjercicio = %s
        AND e.idEstudiante = %s;"""
        variables = (idCourse, idTheme, idExercise, idStudent)
        result = self.executeSQL(query, variables)
        result = result[0]
        detail = ""
        if result[8] is not None:
            detail = result[8]
        feedback = ""
        if result[9] is not None:
            feedback = result[9]
        note = ""
        if result[10] is not None:
            note = result[10]
        NewDelivery = Delivery(result[6], result[7], detail, feedback, note)
        return NewDelivery

    def qualified_exerciseDB(self, nameExercise, CourseName, nameActivity, email):
        idStudent = self.get_id_student_by_emailDB(email)
        idCourse = self.get_id_course_by_nameDB(CourseName)
        idTheme = self.get_id_theme_by_nameDB(nameActivity, idCourse)
        idExercise = self.get_id_exercise_by_nameDB(nameExercise, idTheme, idCourse)
        query = """SELECT COUNT(*) FROM Entrega
        WHERE `estudiante_idEstudiante` = %s
        AND `ejercicio_idEjercicio` = %s
        AND `ejercicio_tematica_idTematica` = %s
        AND `ejercicio_tematica_curso_idCurso` = %s
        AND nota is not null
        AND retroalimentacion is not null;"""
        variables = (idStudent, idExercise, idTheme, idCourse)
        result = self.executeSQL(query, variables)
        quantity = 0
        if result is not None:
            quantity = result[0][0]
        exist = quantity >= 1
        return exist
