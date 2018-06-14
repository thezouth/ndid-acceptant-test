ABCI=./smart-contract
API=./api
EXAMPLE=./examples

update:
	cd $(ABCI); git pull --rebase origin master
	cd $(API); git pull --rebase origin master
	cd $(EXAMPLE); git pull --rebase origin master

checkout:
	cd $(ABCI); git checkout .
	cd $(API); git checkout .
	cd $(EXAMPLE); git checkout .

build:
	cd $(ABCI); docker/build.sh
	cd $(API); docker/build.sh
	cd $(EXAMPLE); docker/build.sh

run: up

up:
	docker-compose -f $(ABCI)/docker/docker-compose.yml up -d
	docker-compose -f $(API)/docker/docker-compose.yml up -d
	docker-compose -f $(EXAMPLE)/docker/docker-compose.yml up -d

down:
	docker-compose -f $(ABCI)/docker/docker-compose.yml down --remove-orphans

test:
	echo $(ABCI)
	echo $(API)
	echo $(EXAMPLE)
