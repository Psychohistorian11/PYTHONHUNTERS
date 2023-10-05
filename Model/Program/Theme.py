from Model.Program.Exercise import Exercise
from DB.ConnectionDB import ConnectionDB


class Theme:
    def __init__(self):
        self.Themes = [{"task": "Variables"}]
        self.Exercises = [{"task": []}]

    def enter_theme(self, newTheme, idCourse):
        ConnectionDB().enter_ThemeDB(newTheme, idCourse)

    def edit_theme(self, theme, newtheme, name_course):
        ConnectionDB().edit_themeDB(theme, newtheme,name_course)

    def delete_theme(self, theme,name_course):
        ConnectionDB().delete_themeDB(theme, name_course)

    def update_themes(self, listThemesfromDB):
        for theme in listThemesfromDB:
            self.Themes.append({'task': theme})

    def create_exercise(self, nameExercise, availability, difficulty, statement):
        new_exercise = Exercise(nameExercise, availability, difficulty, statement)
        return new_exercise

    def update_exercise(self, newExercise):
        self.Exercises.append({'task': [newExercise.nameExercise,
                                        newExercise.availability,
                                        newExercise.difficulty,
                                        newExercise.statement]})

    def create_links(self):
        pass
