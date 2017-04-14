# Ensemble Feedback

### How to setup a project
- install virtualenvwrapper

> pip install virtualenvwrapper

- 檢查是否有裝Postgres

> which psql  


### How to run the app locally
[https://devcenter.heroku.com/articles/getting-started-with-python#run-the-app-locally](https://devcenter.heroku.com/articles/getting-started-with-python#run-the-app-locally)



### How to handle database migrations (by [Flask-Migrate](http://flask-migrate.readthedocs.io/en/latest/) )
- please make sure "environment variables ENV=DEVELOPMENT", which means local database and local server
- init database at *local side*
> python manage.py db init  #only do it at first time
> python manage.py db migrate
> python manage.py db upgrade
- if database scheme changes, do database migration and update
> python manage.py db migrate
> python manage.py db upgrade

- push migrations folder to *server*
> git add migrations/*
> git commit "db migrations"
> git push origin master

- only run db upgrade at remote server
> heroku run python manage.py db upgrade

### How to import local files into remote database
- setup local environment variables
> export ENV=TESTING
> export DATABASE_URL=<db_URL>
> python manage.py import_articles

### How to deal with out of sync between remote db and local db
- check the current version of both databases
- export ENV=DEVELOPMENT
> python manage.py db current
> heroku run python manage.py db current

- check the history of database
> python manage.py db history

-  set the correct version for remote db
> heroku run python manage.py db stamp HEAD or
> heroku run python manage.py db stamp <revision> #Sets the revision in the database to the one given as an argument, without performing any migrations.
> heroku run python manage.py db upgrade

