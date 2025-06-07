# fitnesstudio_backend

# Install Django rest framework

    pip install djangorestframework
    Add 'rest_framework' to your INSTALLED_APPS setting.
    INSTALLED_APPS = [
        ...
        'rest_framework',
    ]
    create project - "django-admin startproject fitnesstudio_backend"
    create app - "python manage.py startapp fitness"
    run project - "python manage.py runserver"

# Postman apis

list classes - http://127.0.0.1:8000/api/fitness-class(GET)
create booking - http://127.0.0.1:8000/api/fitness-class(POST)
list booking based on email - http://127.0.0.1:8000/api/list-client-bookings?client_email=test@gmail.com(GET)
