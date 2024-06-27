include .env

THIS_FILE := $(lastword $(MAKEFILE_LIST))
DOCKER_COMPOSE := docker-compose.yml

.PHONY: build up start down destroy stop restart ps test setup

build:
	docker-compose -f $(DOCKER_COMPOSE) build $(c)
build-full:
	docker-compose -f $(DOCKER_COMPOSE) build $(c) --no-cache
up:
	docker-compose -f $(DOCKER_COMPOSE) up -d $(c)
start:
	docker compose -f $(DOCKER_COMPOSE) build $(c)
	docker compose -f $(DOCKER_COMPOSE) up -d $(c)
down:
	docker-compose -f $(DOCKER_COMPOSE) down $(c)
stop:
	docker-compose -f $(DOCKER_COMPOSE) stop $(c)
restart:
	docker-compose -f $(DOCKER_COMPOSE) down $(c)
	docker-compose -f $(DOCKER_COMPOSE) build $(c)
	docker-compose -f $(DOCKER_COMPOSE) up -d $(c)
ps:
	docker-compose -f $(DOCKER_COMPOSE) ps
setup:
	mysql -h localhost -uroot -p${MYSQL_ROOT_PASSWORD} --protocol=tcp < src/migrations/tables.sql
	mysql -h localhost -uroot -p${MYSQL_ROOT_PASSWORD} --protocol=tcp < src/migrations/initial.sql
test:
	docker exec -w /src/tests safe-foods-api_web_1 pytest -s
type-check:
	docker exec -w /src safe-foods-api-web-1 mypy .
format-check:
	docker exec -w /src safe-foods-api-web-1 autopep8 -r . --diff
format-fix:
	autopep8 -r . --in-place
