import pandas as pd
import numpy as np
from sqlalchemy import create_engine


class assist():

    def upload_df(df_in,tbl_name,batch_size=1000):
        try:
            server = 'tcp:g-server.database.windows.net,1433;'
            database = 'g-demo'
            username = 'luisb'
            password = 'Luis950.#'
            driver_str = "Driver={ODBC Driver 18 for SQL Server}"
            odbc = f"{driver_str};Server={server}Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
            engine=create_engine(f'mssql+pyodbc:///?odbc_connect={odbc}')

            # Insertar el DataFrame en la tabla de la base de datos
            df_in.to_sql(tbl_name, engine, if_exists='replace', index=False, chunksize=batch_size)
        except Exception as e:
            print(f'error upload {e}')
            return False
        return True
        
    
    def load_file(self,df_in,batch_size=1000):
        try:
            df = df_in.copy()
            df = departments.clean(df)
            response = departments.upload_df(df,batch_size=1000)
        except Exception as e:
            return {'uploaded':False, 'err-uploading':e}

        return {'uploaded':True}


class departments():

    def clean(df):
        try:
            df.rename(columns={0: "id", 1: "department"}, inplace=True)
            df['id'] = df['id'].astype(int,errors='ignore')
            df['department'] = np.where(pd.isnull(df['department']),df['department'],df['department'].astype(str, errors='ignore'))
            df = df[['id','department']].copy()
        except Exception as e:
            print(f"error clean: {e}")
            return False

        return df
    
    def upload_df(df_in,batch_size=1000):
        try:
            server = 'tcp:g-server.database.windows.net,1433;'
            database = 'g-demo'
            username = 'luisb'
            password = 'Luis950.#'
            driver_str = "Driver={ODBC Driver 18 for SQL Server}"
            odbc = f"{driver_str};Server={server}Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
            engine=create_engine(f'mssql+pyodbc:///?odbc_connect={odbc}')

            # Insertar el DataFrame en la tabla de la base de datos
            df_in.to_sql('departments', engine, if_exists='replace', index=False, chunksize=batch_size)
        except Exception as e:
            print(f'error upload {e}')
            return False
        return True
        
    
    def load_file(self,df_in,batch_size=1000):
        try:
            df = df_in.copy()
            df = departments.clean(df)
            response = departments.upload_df(df,batch_size=1000)
        except Exception as e:
            return {'uploaded':False, 'err-uploading':e}

        return {'uploaded':True}


class jobs():

    def clean(df):
        try:
            df.rename(columns={0: "id", 1: "job"}, inplace=True)
            df['id'] = df['id'].astype(int,errors='ignore')
            df['job'] = np.where(pd.isnull(df['job']),df['job'],df['job'].astype(str, errors='ignore'))
            df = df[['id','job']].copy()
        except Exception as e:
            print(f"error clean: {e}")
            return False

        return df
    
    def upload_df(df_in,batch_size=1000):
        try:
            server = 'tcp:g-server.database.windows.net,1433;'
            database = 'g-demo'
            username = 'luisb'
            password = 'Luis950.#'
            driver_str = "Driver={ODBC Driver 18 for SQL Server}"
            odbc = f"{driver_str};Server={server}Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
            engine=create_engine(f'mssql+pyodbc:///?odbc_connect={odbc}')

            # Insertar el DataFrame en la tabla de la base de datos
            df_in.to_sql('jobs', engine, if_exists='replace', index=False, chunksize=batch_size)
        except Exception as e:
            print(f'error upload {e}')
            return False
        return True
        
    
    def load_file(self,df_in,batch_size=1000):
        try:
            df = df_in.copy()
            df = jobs.clean(df)
            response = jobs.upload_df(df,batch_size=1000)
        except Exception as e:
            return {'uploaded':False, 'err-uploading':e}

        return {'uploaded':response}



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
            print(f"error clean: {e}")
            return False

        return df
    
    def upload_df(df_in,batch_size=1000):
        try:
            server = 'tcp:g-server.database.windows.net,1433;'
            database = 'g-demo'
            username = 'luisb'
            password = 'Luis950.#'
            driver_str = "Driver={ODBC Driver 18 for SQL Server}"
            odbc = f"{driver_str};Server={server}Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
            engine=create_engine(f'mssql+pyodbc:///?odbc_connect={odbc}')

            # Insertar el DataFrame en la tabla de la base de datos
            df_in.to_sql('hired_employees', engine, if_exists='replace', index=False, chunksize=batch_size)
        except Exception as e:
            print(f'error upload {e}')
            return False
        return True
        
    
    def load_file(self,df_in,batch_size=1000):
        try:
            df = df_in.copy()
            df = employees.clean(df)
            response = employees.upload_df(df,batch_size=batch_size)
        except Exception as e:
            return {'uploaded':False, 'err-uploading':e}

        return {'uploaded':response}




        


