from ModeL import User


class Student(User):
    def __init__(self, firstName, lastName, email, password, score):
        super().__init__(firstName, lastName, email, password)
        self.score = score
