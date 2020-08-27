# djangolab
Template Django REST Framework project

# to-do
- get simple Angular client running that can login

# done
- fix docker startup
- Remove patient and hospital models and replace with generic resource model
- Update corresponding admin pages as well
- make runnable locally (without docker)
- get existing tests working

# how to run the app in debug mode
- open terminal
- make sure you're in the 'djangolab' virtual environment
- go to src/
- type python manage.py runserver

# how to run the app in docker
- open terminal
- type docker-compose up -d
- open web browser and go to http://localhost:8000 (no https yet)

# how to list resources
- open admin panel at http://localhost:8000/admin
- login as admin
- create new resource (generate UUID online somewhere)
- logout
- go to API explorer at http://localhost:8000
- select login > create
- click 'interact' button
- type admin username and password
- copy token
- go to authentication > token
- specify bearer 'JWT' and paste token value
- click send request
- go to resources > list
- click send request
