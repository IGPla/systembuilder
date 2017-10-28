# djangocelery prod

Exposes a django project on production environment through port 80 with celery integration.

## Stack:

- nginx
- uwsgi
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
- nginx: rebuild nginx config files and folders
- uwsgi: rebuild supervisor config files and folders
- celery: rebuild celery config files and folders

## Vars:

- docker_db_name (default: db_prod)
- docker_tasks_queue_name (default: tasks_queue_prod)
- docker_tasks_results_name (default: tasks_results_prod)
- docker_tasks_worker_name (default: tasks_prod)
- docker_proxy_name (default: nginx_prod)
- docker_web_name (default: web_prod)
- docker_host_port (default: 80)

## Example of use:

python3 builder.py --env prod --action start --template djangocelery --flag new --flag always --flag nginx --flag uwsgi --flag celery my_project
