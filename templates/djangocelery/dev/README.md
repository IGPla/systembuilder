# djangocelery dev

Exposes a django project through port 8000 with celery integration.

## Stack:

- celery
- rabbitmq
- redis
- django
- postgres

## Required files:

- systemrequirements.txt in project directory with all system requirements
- requirements.txt in project directoy with all python requirements

## Flags:

- always: required steps for all situations
- new: steps that will be performed only on new projects
- celery: rebuild celery config files and folders

## Vars:

- docker_db_name (default: db_dev)
- docker_tasks_queue_name (default: tasks_queue_dev)
- docker_tasks_results_name (default: tasks_results_dev)
- docker_tasks_worker_name (default: tasks_dev)
- docker_web_name (default: web_dev)
- docker_host_port (default: 8000)

## Example of use:

python3 builder.py --env dev --action start --template djangocelery --flag new --flag always --flag celery my_project
