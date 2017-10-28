# basicdjango prod

Exposes a django project on production environment through port 80.

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

## Vars:

- docker_db_name (default: db_prod)
- docker_web_name (default: web_prod)
- docker_proxy_name (default: nginx_prod)
- docker_host_port (default: 80)

## Example of use:

python3 builder.py --env prod --action start --template basicdjango --flag new --flag always --flag nginx --flag uwsgi my_project
