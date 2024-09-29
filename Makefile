DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yml
STORAGES_FILE = docker_compose/storages.yml
APP_CONTAINER = main-app
KAFKA_FILE = docker_compose/kafka.yml
KAFKA_CONTAINER = kafka

.PNONY: kafka
kafka:
	${DC} -f ${KAFKA_FILE} ${ENV} up --build -d

.PHONY: kafka-logs
kafka-logs:
	${LOGS} ${KAFKA_CONTAINER} -f

.PHONY: messaging-logs
messaging-logs:
	${DC} -f ${KAFKA_FILE} logs -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${KAFKA_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest