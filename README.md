# recipe-app-api

### Clone the repository and don't forget to start your Docker on your system
``` docker-compose build ```
### If you want to build and check for unit test 
``` docker-compose run --rm src sh -c "python manage.py test && flake8" ```
### Runserver the project
``` docker-compose up```