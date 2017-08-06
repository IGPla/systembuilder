# systembuilder
A system builder based on docker compose and templates. With the right template you will be able to start working on your project, completely configured and up to run in seconds
Example:
python3 builder.py --template basicdjango --action start --env prod --flag always --flag new --flag uwsgi --flag nginx my_test_project
You can get more information about each option in the interactive help
python3 builder.py --help
and in each README file in every environment of every template
templates/TEMPLATE_X/ENV_Y/README