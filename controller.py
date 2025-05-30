from app import app
from flask import request, abort, jsonify, render_template
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
        dictinfo['msg'] = "sorry we couldn't upload the file, Only acept .csv"
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
    except Exception as e:
        dictinfo['error'] = True
        dictinfo['msg'] = "sorry we couldn't find the parameter 'file'"
        print(e)

    try:
        dictinfo['chunk'] = int(request.form['chunk'])
        if dictinfo['chunk'] > 1000:
            dictinfo['chunk'] = 1000
    except Exception as e:
        #print(f"error get chunk {e}")
        print('Chunk value not provided or invalid, using default value of 1000')

    return dictinfo


def set_response():
    response = {
        'status': True,
        'error': False,
        'msg':  None,
    }

    return response


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': True, 'msg': 'Welcome to the Employee Management System API. Please use the endpoints to upload data or retrieve reports.'})


@app.route('/upload_departments', methods=['POST'])
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


@app.route('/upload_jobs', methods=['POST'])
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


@app.route('/upload_employees', methods=['POST'])
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


@app.route("/hired_quarter", methods=['GET'])
def hired_quarter():
    response = set_response()
    #get data
    tables = queries()
    status, df_data, err = tables.exec_querie('hired_quarter')
    if not status:
        response['status'] = False
        response['error'] = True
        response['msg'] = err
 
    try:
        if request.headers['Content-Type'] == 'application/json':
            response['data'] = df_data.to_dict(orient='records')
            return jsonify(response)
    except:
        pass
    print(df_data.columns.values)
    return render_template('hired_quarter.html',  tables=[df_data.to_html(classes='data')], 
                           titles=df_data.columns.values, error = response['error'],msg = response['msg'])



@app.route("/hired_department", methods=['GET'])
def hired_department():
    response = set_response()
    #get data
    tables = queries()
    status, df_data, err = tables.exec_querie('hired_department')
    if not status:
        response['status'] = False
        response['error'] = True
        response['msg'] = err

    try:
        if request.headers['Content-Type'] == 'application/json':
            response['data'] = df_data.to_dict(orient='records')
            return jsonify(response)
    except:
        pass
    print(df_data.columns.values)
    return render_template('hired_department.html',  tables=[df_data.to_html(classes='data')], 
                           titles=df_data.columns.values, error = response['error'],msg = response['msg'])