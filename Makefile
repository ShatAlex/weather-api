.SILENT:

build:
	docker-compose up --build
run:
	docker-compose up
db_connect:
	docker-compose exec db bash
run_parser:
	docker exec -it app_weather /usr/local/bin/python src/parser/parser.py