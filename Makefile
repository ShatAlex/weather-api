.SILENT:

build:
	docker-compose up --build
run:
	docker-compose up
run_parser:
	docker exec -it app_weather /usr/local/bin/python src/parser/parser.py