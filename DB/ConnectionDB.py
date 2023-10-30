import mysql.connector

config = {'user': 'bit_busters',
          'password': 'password123',
          'host': 'db4free.net',
          'database': 'pythonbd',
          'port': 3306,  # Puerto predeterminado de MySQL
          'raise_on_warnings': True}  # Para que se generen excepciones en caso de advertencias


class ConnectionDB:
    conn = None
    def _init_(self):
       pass # Mantén la conexión abierta en la instancia

    def connect(self):
        if not self.conn:
            self.conn = mysql.connector.connect(**config)

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def executeSQL(self, consulta_sql, variables_adicionales=None):
        try:
            self.connect()  # Abre la conexión si no está abierta

            if self.conn.is_connected():
                cursor = self.conn.cursor()
                cursor.execute(consulta_sql, variables_adicionales)

                if consulta_sql.strip().upper().startswith("INSERT") or consulta_sql.strip().upper().startswith(
                        "UPDATE") or consulta_sql.strip().upper().startswith(
                        "DELETE") or consulta_sql.strip().upper().startswith("CREATE"):
                    self.conn.commit()
                    return None

                resultados = cursor.fetchall()
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

    # ESTE METODO SOLO INSERTA ESTUDIANTES AL CURSO 1
    def enter_studentDB(self, newStudent):  # Ingresar nuevo estudiante a la  base de datos, no retorna nada
        query = """INSERT INTO `pythonbd`.`Estudiante`
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
        pass

    def enter_ThemeDB(self, newTheme, nameCourse):  # Ingresar nuevo tema a la base de datos, no retorna nada
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        print("este es el id del curso", idCourse)
        query = """INSERT INTO `pythonbd`.`Tematica`
                    VALUES
                    (null,%s,%s);
                    """
        self.executeSQL(query, (idCourse, newTheme))

    def edit_themeDB(self, actualName, newThemeName, nameCourse):
        idTheme = self.get_id_theme_by_nameDB(actualName)
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        query = """UPDATE Tematica SET nombre = %s WHERE (idTematica = %s) and (curso_idCurso = %s);"""
        variables = (newThemeName, idTheme, idCourse)
        self.executeSQL(query, variables)

    def delete_themeDB(self, theme, nameCourse):
        idTheme = self.get_id_theme_by_nameDB(theme)
        idCourse = self.get_id_course_by_nameDB(nameCourse)

        query = """DELETE FROM `pythonbd`.`Tematica`
        WHERE `idTematica` = %s AND `curso_idCurso` = %s;"""
        variables = (idTheme, idCourse)
        self.executeSQL(query, variables)

    def get_themesDB(self, nameCourse):  # Este metodo me entrega todos los temas que se
        # encuentran en la base de datos, necestio solo los nombres
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        query = """select t.nombre from Tematica t
                  where t.curso_idCurso = %s ;"""
        result = self.executeSQL(query, (idCourse,))
        themes = [name[0] for name in result]
        return themes

    def get_id_theme_by_nameDB(self, nameTheme):
        query_by_id_theme = """SELECT idTematica from Tematica t where t.nombre = %s;"""
        listidTheme = self.executeSQL(query_by_id_theme, (nameTheme,))
        idTheme = listidTheme[0][0]
        return idTheme

    def get_id_course_by_nameDB(self, nameCourse):
        query_by_id_course = """SELECT idCurso from Curso c where nombre = %s"""
        listidCourse = self.executeSQL(query_by_id_course, (nameCourse,))
        idCourse = 0
        if listidCourse:
            idCourse = listidCourse[0][0]
        return idCourse

    def enter_exerciseDB(self, newExercise, nameTheme, nameCourse):
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme)
        query = """INSERT INTO `pythonbd`.`Ejercicio`
                  (`idEjercicio`,`tematica_idTematica`,`tematica_curso_idCurso`,`enunciado`) VALUES
                  (null,%s,%s,%s);"""
        variables = (idTheme, idCourse, newExercise)
        self.executeSQL(query, variables)

    def get_exerciseDB(self, nameTheme, nameCourse):  # Este metodo me entrega un diccionario donde la clave puede
        # ser autoincremento y el valor es una lista con los atributos del Ejercicio
        # El parametro IDnameTheme es la clave foranea de la tabla ejercicio para encontrar
        # los ejercicios correspondientes a una actividad
        idCourse = self.get_id_course_by_nameDB(nameCourse)
        idTheme = self.get_id_theme_by_nameDB(nameTheme)
        query = """SELECT e.idEjercicio,e.nombre,e.disponibilidad,e.dificultad,e.enunciado FROM Ejercicio e JOIN Tematica t ON e.tematica_idTematica = t.idTematica WHERE t.idTematica
        = %s and t.curso_idCurso = %s;"""
        lista_resultados = self.executeSQL(query, (idTheme, idCourse))
        diccionario = {}
        valor = None
        for ejercicio in lista_resultados:
            if ejercicio[2] == 0:
                valor = False
            elif ejercicio[2] == 1:
                valor = True
            diccionario[ejercicio[0]] = [ejercicio[1], valor, ejercicio[3], ejercicio[4]]
        # Este diccionario es de prueba
        listExerciseFromDB = {"Ejercicio1": ["nombre1", True, "easy", "Cree"
                                                                      "una variable y asignele un valor"
                                                                      "bolenano"],
                              "Ejercicio2": ["nombre2", True, "easy", "haga un ciclito"],
                              "Ejercicio3": ["nombre3", False, "Very easy", "Qué es un condicional?"]}
        return diccionario

    def get_id_teacher_by_emailDB(self, teacherEmail):
        query = """SELECT idProfesor from Profesor where correo = %s"""
        listidTeacher = self.executeSQL(query, (teacherEmail,))
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

    def enter_courseDB(self, nameCourse):
        # SOLO SQL
        query = """insert into Curso values (null,1,%s)"""
        self.executeSQL(query, (nameCourse,))

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
        courses = [name[0] for name in result]
        return courses

    def update_ranking(self):
        dic = {}
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
        CourseName = results[0][0]
        return CourseName

    def get_object_exercise_by_nameExercise_CourseName(self, nameExercise, CourseName, nameActivity):
        exercise = ["Crear Variables", True, "muy fácil", "Cree una variable y asignele un valor entero"]
        return exercise