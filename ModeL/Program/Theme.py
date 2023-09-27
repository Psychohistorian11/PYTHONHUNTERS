from ModeL.Program.Exercise import Exercise


class Theme:

    def __int__(self, nameTheme):
        self.nameTheme = nameTheme

    def create_exercise(self, nameExercise, availability, difficulty, statement):
        new_exercise = Exercise(nameExercise, availability, difficulty, statement)
        return new_exercise

    def create_links(self):
        pass
