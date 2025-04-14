Requirement of the application:
1. Python 3.13.1
2. Django 5.1
3. Node.js

To run the project:
1. cd to CSCI3100-project path
2. pipenv shell
3. pipenv install djangorestframework
4. pipenv install django-cors-headers
5. ./manage.py runserver

To run the project on React.js
1. cd to poster-web path
2. npm start

Changing model.py run:
1. ./manage.py makemigrations
2. ./manage.py migrate  

Login as admin:
1. http://127.0.0.1:8000/admin
2. username: admin
3. password: admin