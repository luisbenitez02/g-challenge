# Welcome to G-Challenge _by Luis Benitez_
This is an API demo deployed as solution of “Data Engineering Coding Challenge”

There are avalible three endpoints to upload .csv files and twice more to get information about hired employees


## QuickStart
**The service is only avalible on:** [g-demo.azurewebsites.net](g-demo.azurewebsites.net)

_Please check the endopints and methods avalible to do your own requests in the next sections._

## Uploading data
You can upload new data **(only uploads as replace are available)** over the three different tables: departments, jobs and hired_employees

**Structure of table ‘departments’**
| column     | type    | description                                 |
|------------|---------|---------------------------------------------|
| id         | INTEGER | Id of the department                        |
| department | STRING  | Name of the department (255 characters max) |
|            |         |                     |


**Structure of table jobs**
| column | type    | description                          |
|--------|---------|--------------------------------------|
| id     | INTEGER | Id of the job                        |
| job    | STRING  | Name of the job (255 characters max) |
|        |         |                                      |


**Structure of table hired_employees**
| column        | type     | description                                           |
|---------------|----------|-------------------------------------------------------|
| id            | INTEGER  | Id of the employee                                    |
| datetime      | DATETIME | Hire datetime in format Y-m-d[T]:H:M:S[Z]             |
| department_id | INTEGER  | Id of the department which the employee was hired for |
| job_id        | INTEGER  | If of the job wich the employee was hired for         |

**Only .csv files are supported, be sure of upload csv separated  by comma and compatible with the schemas listed before.**

### Load departments [POST]
**Endpint**: https://g-demo.azurewebsites.net/load_departments

**Example of request in Python**
```python
import requests

url = "https://g-demo.azurewebsites.net/load_jobs"

payload = {'chunk': '1000'} #Optional (INSERT chunk-size)
files=[
  ('file',('jobs.csv',open('yourdata/jobs.csv','rb'),'text/csv'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
```

**Succesfull request**
```json
{
    "error": false,
    "file-uploaded": "departments",
    "msg": null,
    "status": true,
    "uploaded": true
}

```

**Failed request**
```json
{
    "error": true,
    "msg": "error <type> [description]",
    "status": false
}
```

### Load departments [POST]
**Endpint**: https://g-demo.azurewebsites.net/load_departments

**Example of request in Python**
```python
import requests

url = "https://g-demo.azurewebsites.net/load_jobs"

payload = {'chunk': '1000'} #Optional (INSERT chunk-size)
files=[
  ('file',('jobs.csv',open('yourdata/jobs.csv','rb'),'text/csv'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
```

**Succesfull request**
```json
{
    "error": false,
    "file-uploaded": "departments",
    "msg": null,
    "status": true,
    "uploaded": true
}

```

**Failed request**
```json
{
    "error": true,
    "msg": "error <type> [description]",
    "status": false
}
```
