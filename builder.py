# -*- coding: utf-8 -*-
"""
Systems builder main script
"""
import argparse
import os
import subprocess
import json

TEMPLATE_DIRECTORY = "templates"
PROJECT_DIRECTORY = "project"
ACTIONS = ["start", "stop", "status", "restart"]
ENVS = ["dev", "prod"]
DOCKER_COMPOSE_FILE = "docker-compose.yml"
CONFIG_FILE = "builderconfig.json"
DEBUG = False

def run_system_command(command):
    """
    Run system command
    """
    if DEBUG:
        print("Executing '%s'" % command)
    subprocess.run(command.split())

def new_file(step, common_params):
    """
    Create new file
    """
    _file = step.get("filename") % common_params
    with open(_file, "w") as fd:
        content = step.get("filecontent") % common_params
        fd.write(content)
    
def replacement(step, common_params):
    """
    Perform replacement step
    """
    _file = step.get("file") % common_params
    with open(_file, "r") as fd:
        lines = fd.readlines()
    to_replace = step.get("replace")
    for key, val in to_replace.items():
        val = val % common_params
        newlines = []
        found = False
        open_lists = 0
        open_dicts = 0
        for line in lines:
            if key in line:
                found = True
                
            if found and "{" in line:
                open_dicts += 1
            if found and "[" in line:
                open_lists += 1
            if found and "}" in line:
                open_dicts -= 1
            if found and "]" in line:
                open_lists -= 1

            if not found:
                newlines.append(line)
            else:
                if not open_dicts and not open_lists:
                    found = False
                    newlines.append(val)
                
        lines = newlines
    with open(_file, "w") as fd:
        for line in lines:
            fd.write(line)
    
def copy_file(step, common_params):
    """
    Perform copy file step
    """
    fromfile = step.get("fromfile") % common_params
    tofile = step.get("tofile") % common_params
    command = "cp %s %s" % (fromfile, tofile)
    run_system_command(command)

def run_command(step, common_params):
    """
    Perform run command step
    """
    command = step.get("command") % common_params
    run_system_command(command)

def run_steps(steps, flags, common_params):
    """
    Run steps
    """
    for step in steps:
        if step.get("flag") in flags:
            action = step.get("action")
            print("Performing step '%s'" % step.get("name"))
            if action == "copyfile":
                copy_file(step, common_params)
            elif action == "runcommand":
                run_command(step, common_params)
            elif action == "replacement":
                replacement(step, common_params)
            elif action == "newfile":
                new_file(step, common_params)
    
def perform_start(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params):
    """
    Perform start action
    """
    for cmd in ["rm %(template_dir)s/project" % common_params,
                "ln -s %(project_dir)s %(template_dir)s" % common_params]:
        run_system_command(cmd)
    steps = config.get("start", [])
    run_steps(steps, flags, common_params)
    command = "%s up -d" % composer_base_command
    run_system_command(command)

def perform_stop(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params):
    """
    Perform stop action
    """
    steps = config.get("stop", [])
    run_steps(steps, flags, common_params)
    command = "%s down" % composer_base_command
    subprocess.run(command.split())

def perform_status(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params):
    """
    Perform status action
    """
    steps = config.get("status", [])
    run_steps(steps, flags, common_params)
    command = "%s ps" % composer_base_command
    subprocess.run(command.split())

def perform_restart(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params):
    """
    Perform restart action
    """
    perform_stop(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params)
    perform_start(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params)
    
def perform_action(base_dir, template_dir, project_dir, composer_file, config_file, action, env, projectname, flags):
    """
    Perform desired action
    """
    composer_base_command = "docker-compose -f %s" % (composer_file,)
    if DEBUG:
        print("Composer base command: '%s'" % composer_base_command) 
    with open(config_file, "r") as fd:
        config = json.loads(fd.read())
    common_params = {'template_dir': template_dir, 'project_dir': project_dir, 'project_name': projectname, 'composer_base_command': composer_base_command}
    if action == "start":
        perform_start(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params)
    elif action == "stop":
        perform_stop(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params)
    elif action == "status":
        perform_status(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params)
    elif action == "restart":
        perform_restart(base_dir, template_dir, project_dir, composer_base_command, action, env, projectname, flags, config, common_params)

def get_base_dir():
    """
    Return base dir
    """
    return os.path.abspath(os.path.dirname(__file__))

def parse_init():
    base_template_dir = os.path.join(get_base_dir(), TEMPLATE_DIRECTORY)
    available_templates = [item for item in os.listdir(base_template_dir) if os.path.isdir(os.path.join(base_template_dir, item))]
    
    parser = argparse.ArgumentParser(description='Create new system based on a template')
    parser.add_argument('--template', action="store", choices=available_templates, required=True)
    parser.add_argument('--action', action="store", choices=ACTIONS, required=True)
    parser.add_argument('--env', action="store", choices=ENVS, required=True)
    parser.add_argument('--flag', action="append", help="Flags to be applied. Only steps with included flags will be executed")
    parser.add_argument('--debug', action="store_true", help="Add this argument to get extra verbosity on each command")
    parser.add_argument('projectname', action="store")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_init()
    template = args.template
    action = args.action
    env = args.env
    projectname = args.projectname
    flags = args.flag
    DEBUG = args.debug
    
    base_dir = get_base_dir()
    templates_dir = os.path.join(base_dir, TEMPLATE_DIRECTORY)
    template_dir = os.path.join(templates_dir, template, env)
    project_dir = os.path.join(base_dir, PROJECT_DIRECTORY)
    composer_file = os.path.join(template_dir, DOCKER_COMPOSE_FILE)
    config_file = os.path.join(template_dir, CONFIG_FILE)

    perform_action(base_dir, template_dir, project_dir, composer_file, config_file, action, env, projectname, flags)
