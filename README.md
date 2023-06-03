# Individual-Pharmaceutical-Care-Plan-Application
App to review currently taken medications for pharmaceutical patients
# Setup of the app
Innstall requirements of the project in terminal:

$ pip install -r requirements.txt

Create a connection to the PostgreSQL database. Create migrations and migrate:

$ python manage.py makemigrations then $ python manage.py migrate

To start the app:

$ python manage.py runserver
