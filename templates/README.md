# How to create new templates:

New templates can be created to achieve any desired service structure. They must follow simple rules, and all will run as expected. These rules are the following:

1. Create a folder for your template. The name you choose will be the template name
2. Create environemnt folders, one for dev and one for prod in your template folder
2. Create a README file in every environment folder to store all information about it
3. Create a docker-compose.yml.template file in every environment root folder with your docker compose build template (prepared to be filled with project vars)
4. Create defaultvars.json with all default values for project vars. Simple dict format
5. Create preserveflags.json with a list of flags that must be preserved
5. Create a builder-config.json file in every environment root folder with all steps for your build. Steps must follow a schema:
{
  "MOMENT": [
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


## Allowed values:

- MOMENT: start, afterstart, stop, afterstop, status, restart (more in "actions" section)
- STEP_NAME: put here what you want
- STEP_FLAG: a flag name (more in "flags" section)
- STEP_ACTION: copyfile, runcommand, replacement, newfile, append (more in "step actions" section)
- REST_OF_OPTIONS: each kind of action have their own custom options

## Moments:

- start: Steps in this moment will be performed before docker starts the service
- afterstart: Steps in this moment will be performed after docker starts the service
- stop: Steps in this moment will be performed before docker stops the service
- afterstop: Steps in this moment will be performed after docker stops the service
- status: Steps in this moment will be performed before check status
- restart: applies start and stop, thus, start steps and stop steps will be performed

## Flags:

Flags are the keywords that you decide to trigger steps. Each step will have a flag. If user use builder.py with a flag "FLAG1", all steps with that flag in the running action will be performed.
In other words, this is a way to categorize a step in a given moment and allow to filter every moment to run only a subset of steps.
preserveflags.json must contain all flags that must be preserved for future calls. They should be the ones that do not destroy or change content.

## Step actions:

Currently there are 5 step actions
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

## Project defined variables:

User can define custom project variables. Each of that allowed variables are described in the README.md inside every environment. That variables will allow user to tune project environment.

## Variables available on your step actions:

There are several variables available while you define your step actions. These are the following:
- template_dir: template base directory. it will be composed as follows /TEMPLATES_FOLDER_ROOT_PATH/TEMPLATE/ENV
- project_dir: project base directory
- project_name: the name of your project
- composer_base_command: base command for docker composer. Useful for "runcommand" step action, when you want to run actions inside your containers (run a command, build container...)
- docker_command_user_fix: fix to be used with your commands inside docker. It's used to fix the issue with root user (it fixes it with current user)
- user_uid: current user uid
- user_gid: current user gid

Additionally, all project defined variables will be available too
