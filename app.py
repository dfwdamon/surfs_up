# import dependencies
from flask import Flask
# create a new instance called app.
app = Flask(__name__)
# create a Flask Route. starting point is root./ is hghest heirarchy level.
@app.route('/')
# create function called hello
def hello_world():
    return 'Hello world'