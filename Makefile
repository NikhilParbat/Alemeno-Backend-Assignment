postgres:
	docker run --name postgres16 --network credit_network -p 5433:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=1111 -d postgres:16-alpine

createdb:
	docker exec -it postgres16 createdb --username=root --owner=root credit_approval

opendb:
	docker exec -it postgres16 psql -U root -d credit_approval

dropdb:
	docker exec -it postgres16 dropdb --username=root credit_approval



.PHONY: createdb postgres dropdb