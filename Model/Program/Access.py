from Model.Student import Student
from DB.ConnectionDB import ConnectionDB


class Access:
    def __init__(self):
        pass

    def register_student(self, firstName, lastName, email, password, score):
        newStudent = Student(firstName, lastName, email, password, score)
        return newStudent

    def enter_student(self, newStudent):
        ConnectionDB().enter_studentDB(newStudent)

    def enter_teacher(self):
        pass
