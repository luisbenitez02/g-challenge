from flask import Flask, render_template, request, send_file, abort, jsonify
from sqlalchemy import create_engine


app = Flask(__name__)

from controller import *

if __name__ == '__main__':
    app.run(debug=True)