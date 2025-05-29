import pytest
import pandas as pd
from models import employees

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
    assert df_cleaned['id'].tolist() == [1, 2]
    assert df_cleaned['name'].tolist() == ['Alice', 'Bob']
    assert pd.api.types.is_datetime64_any_dtype(df_cleaned['datetime'])