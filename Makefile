backend-database-reset:
	docker-compose run --rm backend flask dev recreate-db

backend-test:
	export TRADER_RIMPO_ENV=test
	docker-compose run --rm -e TRADER_RIMPO_ENV backend coverage run -m unittest discover /app/backend/tests

