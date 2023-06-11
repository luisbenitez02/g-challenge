import pandas as pd
import numpy as np
from sqlalchemy import create_engine


class assist():

    def upload_df(self,df_in,tbl_name,batch_size=1000,mode='replace'):
        try:
            server = 'tcp:g-server.database.windows.net,1433;'
            database = 'g-demo'
            username = 'luisb'
            password = 'Luis950.#'
            driver_str = "Driver={ODBC Driver 18 for SQL Server}"
            odbc = f"{driver_str};Server={server}Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
            engine=create_engine(f'mssql+pyodbc:///?odbc_connect={odbc}')

            # Insertar el DataFrame en la tabla de la base de datos
            df_in.to_sql(tbl_name, engine, if_exists=mode, index=False, chunksize=batch_size)
        except Exception as e:
            print(f'error upload {e}')
            return False, f'error uploaded {e}'#TODO error less descriptive
        return True, None


class departments():

    def clean(df):
        try:
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
        df_cleaned,err = departments.clean(df_in)
        if err==True:
            return False,err
        
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
        return status,None
    

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
        return status,None



        


