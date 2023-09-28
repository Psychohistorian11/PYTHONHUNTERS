from Model import User


class Teacher(User):
    def __init__(self, firstName, lastName, email, password):
        super().__init__(firstName, lastName, email, password)
