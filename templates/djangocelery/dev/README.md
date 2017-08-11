# djangocelery dev

Exposes a django project through port 8000 with celery integration.
Stack:
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

Example of use:

python3 builder.py --env dev --action start --template djangocelery --flag new --flag always my_project