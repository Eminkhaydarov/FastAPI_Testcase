.PHONY: converting question stop

converting:
	docker-compose -f converting/docker-compose.yml up --build -d

question:
	docker-compose -f question/docker-compose.yml up --build -d

stop:
	docker-compose -f converting/docker-compose.yml stop
	docker-compose -f question/docker-compose.yml stop