# Import flask dependency
from flask import Flask

# Create a new flask app instance (singular version of something)
app = Flask(__name__) # Variables with underscores before and after them are called magic methods in Python.

# Create flask routes
# 1. Define the starting point (root)
@app.route('/')
# Next, create a function called hello_world(). Whenever you make a route in Flask, you put the code you want in that specific route below @app.route(). 
def hello_world():
    return 'Hello World'
