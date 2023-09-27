from flask import Flask
from DB.ConnectionDB import ConnectionDB
app = Flask(__name__)


class HomeController:

    def __init__(self):
        self.mydb = ConnectionDB
    @staticmethod
    def run():
        app.run(port=3000, debug=True)

    @app.route('/')
    def Index(self):
        return "hello Word"
