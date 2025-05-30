import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from keyvault.keys_admin import get_secrets
import os

print('Getting credentials')
kv_name = 'gdemovault'#os.environ['kv_name']
database = get_secrets(kv_name,'database')
server_name = get_secrets(kv_name,'server')
username = get_secrets(kv_name,'db-username')
password = get_secrets(kv_name,'db-pass')
print('Credentials got')

def get_conection(database,username,password):
    server = f'tcp:{server_name}.database.windows.net,1433;'
    driver_str = "Driver={ODBC Driver 18 for SQL Server}"
    odbc = f"{driver_str};Server={server}Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;ConnectioTimeout=60;"
    engine=create_engine(f'mssql+pyodbc:///?odbc_connect={odbc}')
    return engine

class queries():

    def gen_querie(consult):
        if consult == 'hired_quarter':
            sql_querie = """SELECT d.department AS department,j.job AS job,
                                COUNT(CASE WHEN DATEPART(QUARTER, h.datetime) = 1 THEN 1 END) AS Q1,
                                COUNT(CASE WHEN DATEPART(QUARTER, h.datetime) = 2 THEN 1 END) AS Q2,
                                COUNT(CASE WHEN DATEPART(QUARTER, h.datetime) = 3 THEN 1 END) AS Q3,
                                COUNT(CASE WHEN DATEPART(QUARTER, h.datetime) = 4 THEN 1 END) AS Q4
                            FROM
                                hired_employees h
                                INNER JOIN departments d ON h.department_id = d.id
                                INNER JOIN jobs j ON h.job_id = j.id
                            WHERE
                                YEAR(h.datetime) = 2021
                            GROUP BY
                                d.department,
                                j.job
                            ORDER BY
                                d.department,
                                j.job;"""
            return sql_querie

        elif consult == 'hired_department':
            sql_querie = """SELECT d.id AS id, d.department AS department, COUNT(*) AS hired
                            FROM
                                hired_employees h
                                INNER JOIN departments d ON h.department_id = d.id
                            WHERE
                                YEAR(h.datetime) = 2021
                            GROUP BY
                                d.id,
                                d.department
                            HAVING
                                COUNT(*) > (SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM hired_employees WHERE YEAR(datetime) = 2021 GROUP BY department_id) AS subquery)
                            ORDER BY
                                hired DESC;"""
            return sql_querie
        
    def get_data(querie):
        status = True
        err = None
        try:
            engine = get_conection(database,username,password)
            df_result = pd.read_sql(querie, engine)
        except Exception as e:
            print(e)
            df_result = pd.DataFrame(data={'NODATA': [None]})
            status = False
            err = str(e)
        return status,df_result, err
        
    def exec_querie(self,consult):
        querie = queries.gen_querie(consult)
        status, df_data, err = queries.get_data(querie)
        return status, df_data, err

            
class assist():

    def upload_df(self,df_in,tbl_name,batch_size=1000,mode='replace'):
        try:
            engine=get_conection(database,username,password)
            # Insertar el DataFrame en la tabla de la base de datos
            df_in.to_sql(tbl_name, engine, if_exists=mode, index=False, chunksize=batch_size)
        except Exception as e:
            print(f'error upload {e}')
            return False, f'error uploaded {e}'#TODO error less descriptive
        return True, None


class departments():

    def clean(df):
        try:
            if df.shape[1] > 2:
                msg = "DataFrame must have at most two columns for id and department"
                return None, True, msg
            df.rename(columns={0: "id", 1: "department"}, inplace=True)
            df['id'] = df['id'].astype(int,errors='ignore')
            df['department'] = np.where(pd.isnull(df['department']),df['department'],df['department'].astype(str, errors='ignore'))
            df = df[['id','department']].copy()
        except Exception as e:
            msg = f"error clean: {e}"
            print(msg)
            return None,True,msg #df, err

        return df,False,None
    
    def execute(self,df_in,chunk):
        df_cleaned,err,msg = departments.clean(df_in)
        if err==True:
            return False,msg
        
        helper = assist()
        status,err = helper.upload_df(df_cleaned,'departments',chunk)
        return status,err


class jobs():

    def clean(df):
        try:
            df.rename(columns={0: "id", 1: "job"}, inplace=True)
            df['id'] = df['id'].astype(int,errors='ignore')
            df['job'] = np.where(pd.isnull(df['job']),df['job'],df['job'].astype(str, errors='ignore'))
            df = df[['id','job']].copy()
        except Exception as e:
            msg = f"error clean: {e}"
            print(msg)
            return None,True,msg #df, err

        return df,False,None
    
    def execute(self,df_in,chunk):
        df_cleaned,err,msg = jobs.clean(df_in)
        if err==True:
            return False,msg
        
        helper = assist()
        status,err = helper.upload_df(df_cleaned,'jobs',chunk)
        return status,err
    

class employees():

    def clean(df):
        try:
            df.rename(columns={0: "id", 1: "name",2:"datetime",3:"department_id",4:"job_id"}, inplace=True)
            df['id'] = df['id'].astype(int,errors='ignore')
            df['name'] = np.where(pd.isnull(df['name']),df['name'],df['name'].astype(str, errors='ignore'))
            df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%dT%H:%M:%SZ')
            df['department_id'] = df['department_id'].astype(int,errors='ignore')
            df['job_id'] = df['job_id'].astype(int,errors='ignore')
            df = df[['id','name','datetime','department_id','job_id']].copy()
        except Exception as e:
            msg = f"error clean: {e}"
            print(msg)
            return None,True,msg #df, err

        return df,False,None
    
    def execute(self,df_in,chunk):
        df_cleaned,err,msg = employees.clean(df_in)
        if err==True:
            return False,msg
        
        helper = assist()
        status,err = helper.upload_df(df_cleaned,'hired_employees',chunk)
        return status,err