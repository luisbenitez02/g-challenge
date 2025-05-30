import pytest
import pandas as pd
from models import employees, departments

def test_employees_clean_valid():
    # Dummy dataframe with valid data
    data = {
        0: [5, 7],
        1: ['Luis', 'Viviana'],
        2: ['2025-06-15T10:00:00Z', '2024-03-12T12:30:00Z'],
        3: [2, 5],
        4: [52, 71]
    }
    df = pd.DataFrame(data)
    df_cleaned, err, msg = employees.clean(df)
    #----> tests
    assert err is False
    assert msg is None
    assert list(df_cleaned.columns) == ['id', 'name', 'datetime', 'department_id', 'job_id']
    assert df_cleaned['id'].tolist() == [5, 7]
    assert df_cleaned['name'].tolist() == ['Luis', 'Viviana']
    assert pd.api.types.is_datetime64_any_dtype(df_cleaned['datetime'])#review datatype

#---- check input invalid data  on employees
def test_employees_clean_invalid_date():
    # DataFrame con fecha inválida
    data = {
        0: [2],
        1: ['Sales'],
        2: ['invalid-date'],
    }
    df = pd.DataFrame(data)
    df_cleaned, err, msg = employees.clean(df)
    assert err is True
    assert df_cleaned is None
    assert "error clean" in msg

#----- check input invalid data on departments
def test_departments_clean_invalid_columns():
    # DataFrame con columnas incorrectas
    data = {
        0: [1, 2],
        1: ['HR', 'Finance'],
        2: ['Extra Column', 'Another Extra']
    }
    df = pd.DataFrame(data)
    df_cleaned, err, msg = departments.clean(df)
    assert err is True
    assert df_cleaned is None
    assert "DataFrame must have at most two columns" in msg
