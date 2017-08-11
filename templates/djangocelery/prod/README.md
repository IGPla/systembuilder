# djangocelery prod

Exposes a django project on production environment through port 80 with celery integration.
Stack:
- nginx
- uwsgi
- celery
- rabbitmq
- redis
- django
- postgres

Required files:
- systemrequirements.txt in project directory with all system requirements
- requirements.txt in project directoy with all python requirements

Flags:
- always: required steps for all situations
- new: steps that will be performed only on new projects
- nginx: rebuild nginx config files and folders
- uwsgi: rebuild supervisor config files and folders

Example of use:

python3 builder.py --env prod --action start --template djangocelery --flag new --flag always --flag nginx --flag uwsgi my_project