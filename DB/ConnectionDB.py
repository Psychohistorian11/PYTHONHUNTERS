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

    import mysql.connector

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
                if consulta_sql.strip().upper().startswith("INSERT"):
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

    def verify_accountDB(self, email, password) -> tuple[bool,bool]:
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

    def get_themesDB(self, idCourse):  # Este metodo me entrega todos los temas que se
        # encuentran en la base de datos, necestio solo los nombres
        query = """select t.nombre from Tematica t
                  where t.curso_idCurso = %s ;"""
        result = self.executeSQL(query, (idCourse,))
        themes = [name[0] for name in result]
        print(themes)
        return themes

    def get_id_theme_by_nameDB(self, nameTheme):
        query_by_id_theme = """SELECT idTematica from Tematica where nombre = %s"""
        listidTheme = self.executeSQL(query_by_id_theme, (nameTheme,))
        idTheme = listidTheme[0][0]
        return idTheme

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
        query = """SELECT * FROM Ejercicio e JOIN Tematica t ON e.tematica_idTematica = t.idTematica WHERE t.idTematica = %s and t.curso_idCurso = %s;"""
        lista_resultados = self.executeSQL(query, (idTheme,idCourse))
        # Este diccionario es de prueba
        listExerciseFromDB = {"Ejercicio1": ["Variables", True, "easy", "Cree"
                                                                        "una variable y asignele un valor"
                                                                        "bolenano"],
                              "Ejercicio2": ["Ciclos", True, "easy", "haga un ciclito"],
                              "Ejercicio3": ["Condicionales", False, "Very easy", "Qué es un condicional?"]}
        return listExerciseFromDB

    def enter_courseDB(self, nameCourse):
        pass

    def delete_courseDB(self, nameCourse):
        pass

    def edit_courseDB(self, nameCourse):
        pass

