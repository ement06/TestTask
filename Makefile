.PHONY: help
help:
	@echo 'Makefile for TestTask'
	@echo ''
	@echo '1. Building:'
	@echo '  make setup_venv         (re)Build your environment and setup project'
	@echo ''
	@echo '2. Testing:'
	@echo '  make flake         Check code with flake8'
	@echo ''
	@echo '3. Compile versions:'
	@echo '  make compile-versions    Pin versions of newly added dependencies'
	@echo ''
	@echo '4. Run server'
	@echo '  make runserver            Start local server'
	@echo '5. Building Bot'
	@echo '  make setup_bot_venv       Install bot requirements'

.PHONY: runserver
runserver:
	@echo ' -- Run server'
	venv/bin/python manage.py runserver

.PHONY: setup_venv
setup_venv: clean-files
	@echo ' -- Setting up environment'
	python3.7 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements/requirements.txt
	venv/bin/pip install -r requirements/test_requirements.txt
	@printf ' -- Environment is ready.'

.PHONY: setup_bot_venv
setup_bot_venv: setup_venv
	@echo ' -- Setting up environment'
	venv/bin/pip install -r bot/requirements/requirements.txt
	@printf ' -- Environment is ready.'

clean-files:
	@rm -rf venv/
	@rm -rf *.egg-info


.PHONY: flake
flake:
	venv/bin/flake8 --config=.flake8


.PHONY: compile-versions
compile-versions:
	venv/bin/pip-compile -v --rebuild --no-header --output-file requirements/requirements.txt requirements/requirements.in
	venv/bin/pip-compile -v --rebuild --no-header --output-file requirements/test_requirements.txt requirements/test_requirements.in
