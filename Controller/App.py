from flask import Flask
from Controller.HomeController import HomeController


if __name__ == "__main__":
    Home = HomeController()
    Home.run()



