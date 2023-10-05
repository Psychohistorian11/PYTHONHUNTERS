import mysql.connector

config = {'user': 'bit_busters',
          'password': 'password123',
          'host': 'db4free.net',
          'database': 'pythonbd',
          'port': 3306,  # Puerto predeterminado de MySQL
          'raise_on_warnings': True}  # Para que se generen excepciones en caso de advertencias


class ConnectionDB:

    def __init__(self):
        pass

    def executeSQL(self, consulta_sql, variables_adicionales=None):
        try:
            # Crea una conexión a la base de datos
            conn = mysql.connector.connect(**config)
            if conn.is_connected():
                # Crea un objeto cursor para ejecutar consultas
                cursor = conn.cursor()
                # Ejecuta la consulta

                cursor.execute(consulta_sql, variables_adicionales)

                # Si es una consulta INSERT, no hay resultados para recuperar
                if consulta_sql.strip().upper().startswith("INSERT") or consulta_sql.strip().upper().startswith(
                        "UPDATE") or consulta_sql.strip().upper().startswith(
                    "DELETE") or consulta_sql.strip().upper().startswith("CREATE"):
                    conn.commit()  # Guarda los cambios en la base de datos
                    conn.close()
                    return None  # No hay resultados para devolver

                # Si es otra consulta (SELECT, etc.), recupera los resultados
                resultados = cursor.fetchall()
                conn.close()
                # Imprime los resultados
                return resultados
        except mysql.connector.Error as e:
            print("Error al conectar a la base de datos:", e)

    def verify_accountDB(self, email, password) -> tuple[bool, bool]:
        teacher_query = 'select count(*) from Profesor where correo = %s and contrasenia = %s'
        teacher_results = self.executeSQL(teacher_query, (email, password))
        quantity_teacher = teacher_results[0][0]

        student_query = 'select count(*) from Estudiante where correo = %s and contrasenia = %s'
        student_results = self.executeSQL(student_query, (email, password))
        quantity_student = student_results[0][0]

        existence_teacher = quantity_teacher == 1
        existence_student = quantity_student == 1

        existence = False
        if existence_teacher or existence_student:
            existence = True
        return existence, existence_teacher

    # NO FUNCIONA ESTE METODO
    def enter_studentDB(self, newStudent, idCourse):  # Ingresar nuevo estudiante a la  base de datos, no retorna nada
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
        variables = (idCourse, newStudent.firstName, newStudent.lastName,
                     newStudent.email, newStudent.password, newStudent.score)
        self.executeSQL(query, variables)

    def enter_ThemeDB(self, newTheme, idCourse):  # Ingresar nuevo tema a la base de datos, no retorna nada
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

    def get_themesDB(self, idCourse):  # Este metodo me entrega todos los temas que se
        # encuentran en la base de datos, necestio solo los nombres
        query = """select t.nombre from Tematica t
                  where t.curso_idCurso = %s ;"""
        result = self.executeSQL(query, (idCourse,))
        themes = [name[0] for name in result]
        print(themes)
        return themes

    def get_id_theme_by_nameDB(self, nameTheme):
        query_by_id_theme = """SELECT idTematica from Tematica t where t.nombre = %s;"""
        listidTheme = self.executeSQL(query_by_id_theme, (nameTheme,))
        idTheme = listidTheme[0][0]
        return idTheme

    def get_id_course_by_nameDB(self, nameCourse):
        query_by_id_course = """SELECT idCurso from Curso c where nombre = %s"""
        listidCourse = self.executeSQL(query_by_id_course, (nameCourse,))
        idCourse = listidCourse[0][0]
        return idCourse

    def enter_exerciseDB(self, newExercise, nameTheme, idCourse):
        idTheme = self.get_id_theme_by_nameDB(nameTheme)
        query = """INSERT INTO `pythonbd`.`Ejercicio`
                  (`idEjercicio`,`tematica_idTematica`,`tematica_curso_idCurso`,`enunciado`) VALUES
                  (null,%s,%s,%s);"""
        variables = (idTheme, idCourse, newExercise)
        self.executeSQL(query, variables)

    def get_exerciseDB(self, nameTheme, idCourse):  # Este metodo me entrega un diccionario donde la clave puede
        # ser autoincremento y el valor es una lista con los atributos del Ejercicio
        # El parametro IDnameTheme es la clave foranea de la tabla ejercicio para encontrar
        # los ejercicios correspondientes a una actividad

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
