from app import app
from flask import request
from flask import abort, jsonify

from models import *

@app.route('/load_departments', methods=['POST'])
def load_departments():

    load_response = {
        'read-succeed':True,
    }

    try:
        file = request.files['file']
        df_crud = pd.read_csv(file, header=None)
    except Exception as e:
        err = f'Error load file departments: {e}'
        load_response['error'] = err
        load_response['read-succeed'] = False

    #--- prep data
    db_model = departments()
    response = db_model.load_file(df_crud)
    load_response['uploaded'] = response['uploaded']
    if not load_response['uploaded']:
        load_response['err-uploading'] = response['err-uploading']
    return jsonify(load_response)


@app.route('/load_jobs', methods=['POST'])
def load_jobs():

    load_response = {
        'read-succeed':True,
    }

    try:
        file = request.files['file']
        df_crud = pd.read_csv(file, header=None)
    except Exception as e:
        err = f'Error load file departments: {e}'
        load_response['error'] = err
        load_response['read-succeed'] = False

    #--- prep data
    db_model = jobs()
    response = db_model.load_file(df_crud)
    load_response['uploaded'] = response['uploaded']
    if not load_response['uploaded']:
        load_response['err-uploading'] = response['err-uploading']
    return jsonify(load_response)


@app.route('/load_employees', methods=['POST'])
def load_employees():

    load_response = {
        'read-succeed':True,
    }

    try:
        file = request.files['file']
        df_crud = pd.read_csv(file, header=None)
    except Exception as e:
        err = f'Error load file departments: {e}'
        load_response['error'] = err
        load_response['read-succeed'] = False

    #--- prep data
    db_model = employees()
    response = db_model.load_file(df_crud)
    load_response['uploaded'] = response['uploaded']
    if not load_response['uploaded']:
        load_response['err-uploading'] = response['err-uploading']
    return jsonify(load_response)