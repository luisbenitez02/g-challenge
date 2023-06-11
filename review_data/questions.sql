SELECT
    d.department AS department,
    j.job AS job,
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
    j.job;

#---- question 2
SELECT
    d.id AS id,
    d.department AS department,
    COUNT(*) AS hired
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
    hired DESC;
