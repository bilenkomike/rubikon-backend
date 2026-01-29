# Codnity Django projects template

The project serves purpose of providing a starting boilerplate for developing an API service from scratch
utilising Django Rest Framework as well as service with HTML templates.

These templates represent the following apps:

- `api` app represents the template for API service
- `cars` app represents the template for HTML based web-page

## Technology

### Framework

The current version of the template is based on:

- Python 3.12.*
- Django 5.1.*
- Django Rest Framework 3.15.*
- Pytest 8.3.*

In case of new versions, you are free to update them.

### Database

- Currently, there are applied settings for Postgres server which is defined `settings.py`.
  The developer is free to configure the settings for any database technology that business needs require.

### Dockerization

The template is ready to be used in Docker container. Please, see `docker-compose.yaml` for the services.
You are free to add any new services or modify existing values.


### Swagger

The template has a Swagger integration for automatic API documentation.
The SwaggerUI is accessible via `swagger/`.


### Environment

- The template uses `python-decouple` library for easy management and separation of environment variables.
  All base environment variable names for the template are stored in `example.env` file.
- The template will read the environment variables from the default file `.env` that should be created manually.

### Git

- The template already has `.gitignore` file which holds all the possible folders and cache files that should not be
  pushed to the GitLab.
- The template is ready with the `gitlab-ci.yml` file for the implementation of CI/CD.

### Linters and testing

- Tests should be created utilising Pytest.
- `flake8` and `pycodestyle` is set up to linter the code throughout the project, avoiding migrations and `venv` folder.
- `isort` will automatically sort all the imports throughout the project.
- `tox` is set up to automatize all the linting and testing processes.
- The expected quoting in the template is set to single quotes `' '`. Double quoting will be considered as a style
  error.

## Installation (MacOS/Linux)

### Docker way (preferable):

1. Ensure that you have the latest Docker binaries installed on your computer.

2. Create and fill the `.env` configuration file with the appropriate values. See
   the [example.env](example.env) for the key formats. Ensure, that in the `POSTGRES_HOST`
   key you are defining the Docker database container's name (see [docker-compose.yaml](docker-compose.yaml)).

3. Run docker-compose to build the image and containers.

        docker-compose up

4. See the containers running in Docker. Get the container's ID of the database service and app, copy them.

        docker ps

5. Activate the bash terminal of the database service container.

        docker exec -it <db_container_id> bash

6. Activate Postgres shell.

       psql -U <db_username_from_env> -p
         <db_password>

7. Create database.

       CREATE DATABASE <database_name_as_in_env>;

8. Activate the bash terminal of the app container.

        docker exec -it <app_container_id> bash

9. Migrate data

        python manage.py migrate


10. Create a superuser for the Django admin panel.

        python manage.py createsuperuser

### Local way:

1. Create and fill the `.env` configuration file with the appropriate values. See
   the [example.env](example.env) for the key formats.


2. Create and activate a virtual environment. The current template's Python version is `3.11`.

       python3.11 -m venv venv
       source venv/bin/activate

3. Install requirements.

       pip install -r requirements.txt

4. Migrate migrations.

        python manage.py migrate

5. Create a superuser for the Django admin panel.

        python manage.py createsuperuser


6. Run Django server.

         python manage.py runserver

## Development

1. Remove any of the apps (`api`, `cars`) that are not needed for your development. Their only purpose is to serve as a
   demo app for the expected development structure. Refactor the `settings.py`, `urls.py` file accordingly.
2. Change this readme file according to your developed project needs.

## Testing

1. Tests are expected to be in each app's file `tests.py`.
2. Tests are utilising `Pytest` library.
3. Tests can be launched manually form the app container's bash with `pytest`.
4. Tests and lintering can also be called with `tox` command.

## Deployment

1. Keep a track of your features and changes. Fill the `CHANGELOG.md` giving each ticket/release/fix/feature its own
   version and changelist.
2. Optionally, you can update the version number in `VERSION.txt`, which can be implemented later, for example, in the
   templates or GitLab CI/CD for the tagging.
3. Before the pushing to the remote, call the `tox` command (if using Docker, the command should be called from the
   container's bash. This command will:

- call `isort` library to go through the code and will sort your imports according to PEP8 standard
- call `flake8` and `pycodestyle` to check your code styling, quotes, indentations, unused imports etc. following the
  PEP8 guidelines
- call all the unit tests you have defined in `tests.py` file.

4. `flake8` rules can be changed in `.flake8` file.
5. Tox rules can be changed in `tox.ini`.
