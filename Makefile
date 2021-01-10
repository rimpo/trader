backend-database-reset:
	docker-compose run --rm backend flask dev recreate-db

