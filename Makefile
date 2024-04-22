DOCKER=docker-compose
RUN=run --rm web
MANAGE=python manage.py

# URL WITH DEFAULT VALUE
URL?=https://drive.usercontent.google.com/u/0/uc\?id\=18Ss9afYL8xTeyVd0ZTfFX9dqja4pBGVp\&export\=download

# LOCALLY
run:
	poetry run python src/manage.py runserver
install:
	poetry install
migrate:
	poetry run python src/manage.py migrate
migrations:
	poetry run python src/manage.py makemigrations
test:
	poetry run python src/manage.py test
superuser:
	poetry run python src/manage.py createsuperuser
shell:
	poetry run python src/manage.py shell

# IN DOCKER
docker_up:
	$(DOCKER) up
docker_build:
	$(DOCKER) build
docker_shell:
	$(DOCKER) $(RUN) $(MANAGE) shell
docker_migrate:
	$(DOCKER) $(RUN) $(MANAGE) migrate
docker_makemigrations:
	 $(DOCKER) $(RUN) $(MANAGE) makemigrations
docker_superuser:
	$(DOCKER) $(RUN) $(MANAGE) createsuperuser

# MAIN PROCESS
docker_process_log:
	$(DOCKER) $(RUN) $(MANAGE) process_log $(URL)


# TESTS
docker_tests:
	$(DOCKER) $(RUN) $(MANAGE) test

# LINT
lint:
	poetry run pre-commit run --all-files
