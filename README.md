# Project 10 of the OpenClassrooms Python developper training

## Develop a secured RESTFul API the Django REST Framework

This project is a RESTFul API using the Django REST Framework for python.
It also uses SQLite to store data.
It uses Ppipenv for code versionning en virtual environnement management.

Beware : a demo database is included in the repository, if you do not want the data you will need to erase it with the following command after the setup of the project.
```
django-admin flush
``` 

## Installation

### Sources

In order to run the application, clone the following repository in the directory where you want the application to be stored : https://github.com/chpancrate/ocrpy_project10


### Environment setup 

The application runs with Python 3.11.

To install python you can download it here : https://www.python.org/downloads/

If you are new to Python you can find information here : https://www.python.org/about/gettingstarted/ 

It is better to run the application in a virtual environment. You can find information on virtual envrionments here : https://docs.python.org/3/library/venv.html 

Once in your virtual environment, the following modules are mandatory :
- Django : 4.2.3
- djangorestframework : 3.14.0
- djangorestframework-simplejwt : 5.2.2

All the useful modules are in the requirements.txt file. A quick way to install them is to run the command below in a python terminal:
```
pip install -r requirements.txt
```

## How to run the API

In order to run the application once the setup is complete go in the directory where the application is installed and then use the command : 
```
python manage.py runserver
```

The application will then be accessible at the url : http://127.0.0.1:8000/

## API manual

### Available endpoints

- <int:pk> or <uuid:pk> is the id of the acessed item
- <int:project_pk> is the project id of the accessed contributor or issue
- <int:issue_pk> is the issue id of the accessed comment

| endpoint | actions | authorization | results
| --- | --- | --- | ---
| [USER](#user-enpoint) | | 
| api/user/ | POST | unexisting user or superuser | create user
| api/user/ | GET | superuser | list of users
| api/user/<int:pk>/ | GET | user or superuser | details
| api/user/<int:pk>/ | PATCH | user or superuser
| api/user/<int:pk>/ | PUT | user or superuser
| api/user/<int:pk>/ | DELETE | user or superuser
| [PROJECT](#project-enpoint) | | 
| api/project/ | POST | connected user | the user becomes author and contributor to the project created
| api/project/ | GET | connected user | list of all projects
| api/project/<int:pk>/ | GET | project contributor | details of the project with issues and contributors sublist
| api/project/<int:pk>/ | PATCH | project author
| api/project/<int:pk>/ | PUT | project author
| api/project/<int:pk>/ | DELETE | project author
| [CONTRIBUTOR](#contributor-enpoint) | | 
| api/contributor/<int:project_pk>/ | POST | non contributor for self or contributor for another 
| api/contributor/<int:project_pk>/ | GET | contributor
| api/contributor/<int:project_pk>/<int:pk>/ | GET | user concerned
| api/contributor/<int:project_pk>/<int:pk>/ | DELETE | user concerned
| [ISSUE](#issue-enpoint) | | 
| api/issue/<int:project_pk>/ | POST | project contributor | the user becomes author of the issue created
| api/issue/<int:project_pk>/ | GET | project contributor
| api/issue/<int:project_pk>/<int:pk>/ | GET | project contributor | details of the issue with a comments sublist
| api/issue/<int:project_pk>/<int:pk>/ | PATCH | issue author
| api/issue/<int:project_pk>/<int:pk>/ | PUT | issue author
| api/issue/<int:project_pk>/<int:pk>/ | DELETE | issue author
| [COMMENT](#comment-enpoint) | | 
| api/comment/<int:issue_pk>/ | POST | project contributor | the user becomes author of the comment created
| api/comment/<int:issue_pk>/ | GET | project contributor
| api/comment/<int:issue_pk>/<uuid:pk>/ | GET | project contributor
| api/comment/<int:issue_pk>/<uuid:pk>/ | PATCH | comment author
| api/comment/<int:issue_pk>/<uuid:pk>/ | PUT | comment author
| api/comment/<int:issue_pk>/<uuid:pk>/ | DELETE | comment author

### User enpoint
| Data | rules
| --- | ---
| username | mandatory |
| password | mandatory |
| age | mandatory, >= 15 |
| can_be_contacted | boolean, optional, default = False
| can_data_be_shared | boolean, optional, default = False
| created_time | auto generated

### Project enpoint
| Data | rules
| --- | ---
| author | automatically set to the user creating the project |
| name | mandatory |
| description | optional |
| type | mandatory, must be in list ['back-end', 'front-end', 'ios', 'android']|
| created_time | auto generated |
| updated_time | auto generated |
### Contributor enpoint
| Data | rules
| --- | ---
| user | mandatory, must be an existing user |
| project| at creation retrieved from the url |
| created_time | auto generated |
| updated_time | auto generated |
### Issue enpoint
| Data | rules
| --- | ---
| project | at creation retrieved from the url |
| name |  |
| description |  |
| author | automatically set at creation to the user creating the issue |
| status |  optional, must be in list ['to-do', 'in-progress', 'finished'], default to 'to-do'|
| priority |  optional, must be in list ['low', 'medium', high']|
| assigned_to | must be a user contributor to the project |
| tag | optional, must be in list ['bug', 'feature', 'task'] |
| created_time | auto generated |
| updated_time | auto generated |
### Comment enpoint
| Data | rules
| --- | ---
| issue | at creation retrieved from the url |
| description | mandatory |
| author | automatically set at creation to the user creating the comment |
| created_time | auto generated |
| updated_time | auto generated |
## Users and passwords
Some users are setup, they can be found in the file users.txt in the authentication folder.

