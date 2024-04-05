up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build --no-cache

build-base:
    DOCKER_BUILDKIT=1 docker build -t poke-berry -f Dockerfile .

bash:
	docker-compose run --rm api bash

test:
	docker-compose run --rm api python -m pytest test/

start-build:
	make build-base && make build

checkout-pull:
	set -e
	git checkout $(env)
	git pull
