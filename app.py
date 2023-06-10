from flask import Flask
from flask import Flask, render_template, request, send_file
from sqlalchemy import create_engine
from flask import abort, jsonify

app = Flask(__name__)

from controller import *

if __name__ == '__main__':
    app.run(debug=True)