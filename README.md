# todo_app

"""Create virtual environment and activate it"""

python -m venv venv

venv\Scripts\Activate (Windows)



""" Install requiremnts"""

pip install requirements.txt



""" Makigrations and migrate it"""

python manage.py makemigrations

python manage.py migrate



"""Create superuser"""

python manage.py createsuperuser



""" Run the server"""

python manage.py runserver

# Test your server on http://127.0.0.1:8000/swaager/

## if api not working on postman then you can try it using swagger also.
