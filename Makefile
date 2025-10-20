.PHONY: dj-run build up up-build down ps shell logs dj-logs celery-worker-logs

dj-run:
	python manage.py runserver

build:
	docker compose -f build/docker-compose.yaml build

up:
	docker compose -f build/docker-compose.yaml up -d

up-build:
	docker compose -f build/docker-compose.yaml up -d --build

down:
	docker compose -f build/docker-compose.yaml down

ps:
	docker compose -f build/docker-compose.yaml ps -a

shell:
	docker compose -f build/docker-compose.yaml exec -it backend python manage.py shell

logs:
	docker compose -f build/docker-compose.yaml logs -f 

dj-logs:
	docker compose -f build/docker-compose.yaml logs -f backend

celery-worker-logs:
	docker compose -f build/docker-compose.yaml logs -f celery_worker