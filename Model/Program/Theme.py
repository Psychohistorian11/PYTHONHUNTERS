from Model.Program.Exercise import Exercise
from DB.ConnectionDB import ConnectionDB

DB = ConnectionDB()


class Theme:
    def __init__(self):
        self.Themes = []

        self.Exercises = []

    def enter_theme(self, newTheme, idCourse):
        DB.enter_ThemeDB(newTheme, idCourse)

    def edit_theme(self, theme, newTheme, name_course):
        DB.edit_themeDB(theme, newTheme, name_course)

    def delete_theme(self, theme, name_course):
        DB.delete_themeDB(theme, name_course)

    def update_themes(self, CourseName):
        themes_from_db = DB.get_themesDB(CourseName)
        self.Themes = [{'task': course} for course in themes_from_db]

    def create_exercise(self, nameExercise, availability, difficulty, statement):
        new_exercise = Exercise(nameExercise, availability, difficulty, statement)
        return new_exercise

    def clear_themes(self):
        self.Themes = []

    def enter_exercise(self, nameExercise, emailStudent, nameTheme, nameCourse, code, detail):
        DB.submit_exercise(nameExercise, emailStudent, nameTheme, nameCourse, code, detail)

    def update_exercise(self, listOfExercise):
        print(listOfExercise)
        for exercise in listOfExercise:
            self.Exercises.append({'task': [exercise.nameExercise,
                                            exercise.availability,
                                            exercise.difficulty,
                                            exercise.statement]})

    def get_exercise(self, nameTheme, nameCourse):
        listExercisesFromDB = DB.get_exerciseDB(nameTheme, nameCourse)
        return listExercisesFromDB

    def edit_exercise(self):
        pass

    def create_links(self):
        pass
