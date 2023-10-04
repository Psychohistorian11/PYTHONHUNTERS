from DB.ConnectionDB import ConnectionDB

class Course:
    def __init__(self):
        self.courses = [{"task": "Grupo_63", "done": True}]

    def enter_course(self, nameCourse):
        ConnectionDB().enter_courseDB(nameCourse)