"""
Command usages sequentially

pip install pipenv => install pipenv

pipenv install django => created virutal environment

pipenv shell => activate virtual environment

django-admin startproject storeshow . => created django project, for details => django-admin => for using . django dont create another parent folder

python manage.py runserver 1200 = run the server at port no 1200

pipenv --venv = > get the loaction of the project virtual environment

python manage.py startapp testapp - create another app from django

pipenv install django-debug-toolbar => django debugging

python manage.py makemigrations => django look that every model and create migration files

python manage.py migrate => Generate datbase schema aka tables based on models codes

python manage.py migrate store 002 => Last migration Unapplied in case I want to unapplied from 003 , but remind that it could not reverse the code and created files

pipenv install mysqlclient => connect to mysql with django project

python manage.py makemigrations store --empty => creating empty migration to run custom sql
https://www.mockaroo.com/ => for generate dummy data for the sql database ,this is the web address


"""