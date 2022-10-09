src_dir := $(patsubst %/,%, $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))

.PHONY: venv

mypy:
	poetry run mypy --config-file=$(src_dir)/mypy.ini src

pylint:
	poetry run pylint --rcfile=$(src_dir)/pylintrc src

test:
	poetry run pytest tests

check: mypy pylint test

black:
	poetry run black src

isort:
	poetry run isort --profile black src

format:	isort black

venv:
	python3 -m venv venv
	./venv/bin/pip3 install --requirement requirements.txt --requirement requirements-dev.txt

install:
	poetry install --no-dev

run:
	poetry run python3 src/main.py
