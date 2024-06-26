#!make

help: _header
	${info }
	@echo Opciones:
	@echo ----------------------
	@echo build
	@echo start / stop / restart
	@echo workspace
	@echo logs
	@echo clean
	@echo ----------------------

_header:
	@echo -----
	@echo Flask
	@echo -----

_urls:
	${info }
	@echo -----------------------------
	@echo [Flask] http://localhost:5000
	@echo -----------------------------

build:
	@docker compose build --pull

_start-command:
	@docker compose up -d

start: _start-command _urls

stop:
	@docker compose stop

restart: stop start

workspace:
	@docker compose exec flask /bin/bash

logs:
	@docker compose logs flask

clean:
	@docker compose down -v --remove-orphans
