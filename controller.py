from app import app
from flask import request
from flask import abort, jsonify

from models import *


def load_file(file):
    dictinfo = {
        'error': None,
        'msg':  None,
        'df': None
    }
    try:
        dictinfo['df'] = pd.read_csv(file, header=None)
    except Exception as e:
        dictinfo['error'] = True
        dictinfo['msg'] = "sorry we couldn't load the file, Only acept .csv"
        print(e)
    return  dictinfo


def get_params(req):
    dictinfo = {
        'error': False,
        'msg':  None,
        'file': None,
        'chunk':1000
    }
    
    try:
        dictinfo['file'] = req.files['file']
    except:
        dictinfo['error'] = True
        dictinfo['msg'] = "sorry we couldn't find the parameter 'file'"

    try:
        dictinfo['chunk'] = int(request.form['chunk'])
        if dictinfo['chunk'] > 1000:
            dictinfo['chunk'] = 1000
    except Exception as e:
        print(f"error get chunk {e}")

    return dictinfo


def set_response():
    response = {
        'status': True,
        'error': False,
        'msg':  None,
    }

    return response


@app.route('/load_departments', methods=['POST'])
def load_departments():
    response = set_response()
    get_inf = get_params(request)

    if get_inf['error']:
        response['status'] = False
        response['error'] = get_inf['error']
        response['msg'] = get_inf['msg']
        return jsonify(response)

    df_inf = load_file(get_inf['file'])
    if df_inf['error']:
        response['status'] = False
        response['error'] = get_inf['error']
        response['msg'] = get_inf['msg']
        return jsonify(response)
    
    #--- prep data
    db_model = departments()
    up_resp,err = db_model.execute(df_inf['df'],get_inf['chunk'])
    if not up_resp:
        response['status'] = False
        response['error'] = True
        response['msg'] = err
        return jsonify(response)

    response['uploaded'] = True
    response['file-uploaded'] = 'departments'

    return jsonify(response)


@app.route('/load_jobs', methods=['POST'])
def load_jobs():
    response = set_response()
    get_inf = get_params(request)

    if get_inf['error']:
        response['status'] = False
        response['error'] = get_inf['error']
        response['msg'] = get_inf['msg']
        return jsonify(response)

    df_inf = load_file(get_inf['file'])
    if df_inf['error']:
        response['status'] = False
        response['error'] = get_inf['error']
        response['msg'] = get_inf['msg']
        return jsonify(response)
    
    #--- prep data
    db_model = jobs()
    up_resp,err = db_model.execute(df_inf['df'],get_inf['chunk'])
    if not up_resp:
        response['status'] = False
        response['error'] = True
        response['msg'] = err
        return jsonify(response)

    response['uploaded'] = True
    response['file-uploaded'] = 'jobs'

    return jsonify(response)


@app.route('/load_employees', methods=['POST'])
def load_employees():

    response = set_response()
    get_inf = get_params(request)

    if get_inf['error']:
        response['status'] = False
        response['error'] = get_inf['error']
        response['msg'] = get_inf['msg']
        return jsonify(response)

    df_inf = load_file(get_inf['file'])
    if df_inf['error']:
        response['status'] = False
        response['error'] = get_inf['error']
        response['msg'] = get_inf['msg']
        return jsonify(response)
    
    #--- prep data
    db_model = employees()
    up_resp,err = db_model.execute(df_inf['df'],get_inf['chunk'])
    if not up_resp:
        response['status'] = False
        response['error'] = True
        response['msg'] = err
        return jsonify(response)

    response['uploaded'] = True
    response['file-uploaded'] = 'hired_employees'

    return jsonify(response)