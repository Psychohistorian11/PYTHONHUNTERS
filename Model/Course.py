from DB.ConnectionDB import ConnectionDB

DB = ConnectionDB()


class Course:
    def __init__(self):
        self.courses = []

    def enter_course(self, email, nameCourse):
        DB.enter_courseDB(email, nameCourse)

    def edit_course(self, nameCourse, newCourse):
        DB.edit_courseDB(nameCourse, newCourse)

    def delete_course(self, nameCourse):
        DB.delete_courseDB(nameCourse)

    def updateList(self, email):
        courses_from_db = DB.get_coursesDB(email)
        self.courses = [{"task": course} for course in courses_from_db]

    def clearTheme(self):
        self.courses = []
