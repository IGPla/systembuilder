#How to create new templates:

New templates can be created to achieve any desired service structure. They must follow simple rules, and all will run as expected. These rules are the following:

1. Create a folder for your template. The name you choose will be the template name
2. Create environemnt folders, one for dev and one for prod in your template folder
2. Create a README file in every environment folder to store all information about it
3. Create a docker-compose.yml file in every environment root folder with your docker compose build
4. Create a builder-config.json file in every environment root folder with all steps for your build. Steps must follow a schema:
{
  "ACTION": [
    {
      "name": "STEP_NAME",
      "flag": "STEP_FLAG",
      "action": "STEP_ACTION",
      REST_OF_OPTIONS
    },
    ...
  ],
  "ACTION": [
  	    ...
  ],
  ...
}

Allowed values:

- ACTION: start, stop, status, restart (more in "actions" section)
- STEP_NAME: put here what you want
- STEP_FLAG: a flag name (more in "flags" section)
- STEP_ACTION: copyfile, runcommand, replacement, newfile, append (more in "step actions" section)
- REST_OF_OPTIONS: each kind of action have their own custom options

Actions:

- start: this action starts the service with all dependencies. Steps with this action will be performed before docker starts the service
- stop: this action stops the service with all dependencies. Steps with this action will be performed before docker stops the service
- status: this actions reads the status of the service. Steps with this action will be performed before check
- restart: applies start and stop, thus, start steps and stop steps will be performed

Flags:

Flags are the keywords that you decide to trigger events. Each step will have a flag. If user use builder.py with a flag "FLAG1", all steps with that flag in the running action will be performed.
In other words, is a way to categorize a step in a given action and allow to filter every action to run only a subset of steps.

Step actions:

Currently there are 4 step actions
1. copyfile: performs a copy of a file. It is useful to move files in and out, allowing your docker images to be dynamic in their compilation. Required fields:
  - fromfile: filepath of the source file
  - tofile: filepath for the destiny file
2. runcommand: run a command. Required fields:
  - command: command to be executed
3. replacement: replace a file content with keyword (and given content) with your replacement. Required fields:
  - file: file where we will replace some content
  - replace: dictionary structure, with key as the keyword to be replaced plus content, and value as the replacement
4. newfile: create new file and put content in it. Required fields:
  - filename: file path of the file that will be created
  - filecontent: content that will fill the file
5. append: append filecontent to the end of the file. Required fields:
  - filename: file path of the file that will be updated
  - filecontent: content that will be appened to file
  
Variables available on your step actions:

There are several variables available while you define your step actions. These are the following:
- template_dir: template base directory. it will be composed as follows /TEMPLATES_FOLDER_ROOT_PATH/TEMPLATE/ENV
- project_dir: project base directory
- project_name: the name of your project
- composer_base_command: base command for docker composer. Useful for "runcommand" step action, when you want to run actions inside your containers (run a command, build container...)