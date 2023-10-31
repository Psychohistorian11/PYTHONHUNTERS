from Model.Program.Exercise import Exercise
from DB.ConnectionDB import ConnectionDB

DB = ConnectionDB()


class Theme:
    def __init__(self):
        self.Themes = []

        self.Exercises = [{"task": ["Hello World2",
                                    True,
                                    "muy facil",
                                    "Escriba en la consola Hello World"]}]

    def enter_theme(self, newTheme, idCourse):
        ConnectionDB().enter_ThemeDB(newTheme, idCourse)

    def edit_theme(self, theme, newtheme, name_course):
        ConnectionDB().edit_themeDB(theme, newtheme, name_course)

    def delete_theme(self, theme, name_course):
        ConnectionDB().delete_themeDB(theme, name_course)

    def update_themes(self, CourseName):
        themes_from_db = DB.get_themesDB(CourseName)
        self.Themes = [{'task': course} for course in themes_from_db]

    def create_exercise(self, nameExercise, availability, difficulty, statement):
        new_exercise = Exercise(nameExercise, availability, difficulty, statement)
        return new_exercise

    def clear_themes(self):
        self.Themes = []

    def update_exercise(self, listOfExercise):
        for exercise in listOfExercise:
            self.Exercises.append({'task': [exercise.nameExercise,
                                            exercise.availability,
                                            exercise.difficulty,
                                            exercise.statement]})


    def edit_exercise(self):
        pass

    def create_links(self):
        pass
