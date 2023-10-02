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

    def executeSQL(self, consulta_sql, variables_acidicionales=None):
        try:
            # Crea una conexión a la base de datos
            conn = mysql.connector.connect(**config)
            if conn.is_connected():
                # Crea un objeto cursor para ejecutar consultas
                cursor = conn.cursor()
                # Ejecuta la consulta
                cursor.execute(consulta_sql, variables_acidicionales)
                # Recupera los resultados de la consulta
                resultados = cursor.fetchall()
                conn.close()
                # Imprime los resultados
                return resultados
        except mysql.connector.Error as e:
            print("Error al conectar a la base de datos:", e)

    def verify_accountDB(self, email, password) -> tuple[bool, bool]:
        """

        :rtype: object
        """
        query = 'select count(*) from Profesor where correo = %s and contrasenia = %s'
        results = self.executeSQL(query, (email, password))
        # Verificar si se encontró al menos un usuario
        quantity_teacher = results[0][0]
        # Falta el del profe
        quantity_student = 4
        existence_teacher = quantity_teacher == 1
        existence_student = quantity_student == 1
        existence = False
        if existence_teacher or existence_student:
            existence = True
        return existence, existence_teacher

    def enter_studentDB(self, newStudent):  # Ingresar nuevo estudiante a la  base de datos, no retorna nada
        pass

    def enter_ThemeDB(self, newTheme, idCourse):  # Ingresar nuevo tema a la base de datos, no retorna nada
        pass

    def get_themesDB(self):  # Este metodo me entrega todos los temas que se
        # encuentran en la base de datos, necestio solo los nombres
        listThemesFromDB = ["Arreglos"]
        return listThemesFromDB

    def enter_exerciseDB(self, newExercise, IDnameTheme):
        pass  # Ingresar nuevo Ejercicio

    def get_exerciseDB(self, IDnameTheme):  # Este metodo me entrega un diccionario donde la clave puede
        # ser autoincremento y el valor es una lista con los atributos del Ejercicio
        #El parametro IDnameTheme es la clave foranea de la tabla ejercicio para encontrar
        #los ejercicios correspondientes a una actividad

        #Este diccionario es de prueba
        listExerciseFromDB = {"Ejercicio1": ["Variables", True, "easy", "Cree"
                                                                       "una vairiable y asignele un valor"
                                                                       "bolenano"],
                               "Ejercicio2": ["Ciclos", True, "easy", "haga un ciclito"],
                               "Ejercicio3": ["Condicionales", False,"Very easy", "Qué es un condicional?"]}
        return listExerciseFromDB
