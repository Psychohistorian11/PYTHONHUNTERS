from Model.Program.Exercise import Exercise
from DB.ConnectionDB import ConnectionDB


class Theme:
    def __init__(self):
        self.Themes = [{"task": "Primera Actividad"}]

    def enter_Theme(self, newTheme):
        ConnectionDB().enter_ThemeDB(newTheme)

    def updateThemes(self, listThemesfromDB):
        for theme in listThemesfromDB:
            self.Themes.append({'task': theme})

    def create_exercise(self, nameExercise, availability, difficulty, statement):
        new_exercise = Exercise(nameExercise, availability, difficulty, statement)
        return new_exercise

    def create_links(self):
        pass
