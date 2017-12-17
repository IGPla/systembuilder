# System Builder

A system builder based on docker compose and templates. With the right template you will be able to start working on your project, completely configured and up to run in seconds

Example:

```
python3 builder.py --template basicdjango --action start --env prod --flag always --flag new --flag uwsgi --flag nginx my_test_project
```

You can get more information about each option in the interactive help

```
python3 builder.py --help
```

and in each README file in every environment of every template

templates/TEMPLATE_X/ENV_Y/README

A tool to create new template scaffold is added. It's called newtemplate.py. To use it, just type the following

```
python3 newtemplate.py YOUR_NEW_TEMPLATE_NAME
```

To run commands inside docker containers, there's a tool created for this purpose

```
python3 commander DOCKER_CONTAINER_NAME "COMMAND"
```

Where DOCKER_CONTAINER_NAME can be retrieved from builder.py status action and command is an arbitratry command that will run in the provided container

IMPORTANT NOTE: all scripts in this project are created using python3. Compatibility with python2 is not warranted.
