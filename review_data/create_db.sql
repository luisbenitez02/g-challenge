--create departments
IF OBJECT_ID('departments', 'U') IS NOT NULL
    DROP TABLE departments;

CREATE TABLE departments (
    Id INTEGER,
    department VARCHAR(255)
);

--create hired_employees
IF OBJECT_ID('hired_employees', 'U') IS NOT NULL
    DROP TABLE hired_employees;

CREATE TABLE hired_employees (
    id INTEGER,
    name VARCHAR(255),
    datetime datetimeoffset,
    department_id INTEGER,
    job_id INTEGER
);

--create jobs
IF OBJECT_ID('jobs', 'U') IS NOT NULL
    DROP TABLE jobs;

CREATE TABLE jobs (
    id INTEGER,
    job VARCHAR(255),
);