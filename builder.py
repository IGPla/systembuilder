# -*- coding: utf-8 -*-
"""
Systems builder main script
"""
import argparse
import os
import pwd
import subprocess
import json
import utils
import time

TEMPLATE_DIRECTORY = "templates"
PROJECT_DIRECTORY = "project"
ACTIONS = ["start", "stop", "status", "restart"]
ENVS = ["dev", "prod"]
DOCKER_COMPOSE_FILE = "docker-compose.yml"
DOCKER_COMPOSE_TEMPLATE_FILE = "docker-compose.yml.template"
CONFIG_FILE = "builderconfig.json"
DEBUG = False


def run_system_command(command):
    """
    Run system command
    """
    if DEBUG:
        print("Executing '%s'" % command)
    subprocess.run(command.split())


def append(step, common_params):
    """
    Append content to file
    """
    _file = step.get("file") % common_params
    with open(_file, "a") as fd:
        content = step.get("filecontent") % common_params
        fd.write(content)


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
            elif action == "append":
                append(step, common_params)


def perform_start(base_dir, template_dir, project_dir, composer_base_command,
                  action, env, projectname, flags, config, common_params):
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
    time.sleep(2)  # Time to wait for all services to be up
    steps = config.get("afterstart", [])
    run_steps(steps, flags, common_params)


def perform_stop(base_dir, template_dir, project_dir, composer_base_command,
                 action, env, projectname, flags, config, common_params):
    """
    Perform stop action
    """
    steps = config.get("stop", [])
    run_steps(steps, flags, common_params)
    command = "%s down" % composer_base_command
    subprocess.run(command.split())
    time.sleep(2)  # Time to wait for services to die
    steps = config.get("afterstop", [])
    run_steps(steps, flags, common_params)


def perform_status(base_dir, template_dir, project_dir, composer_base_command,
                   action, env, projectname, flags, config, common_params):
    """
    Perform status action
    """
    steps = config.get("status", [])
    run_steps(steps, flags, common_params)
    command = "%s ps" % composer_base_command
    subprocess.run(command.split())


def perform_restart(base_dir, template_dir, project_dir, composer_base_command,
                    action, env, projectname, flags, config, common_params):
    """
    Perform restart action
    """
    perform_stop(base_dir, template_dir, project_dir, composer_base_command,
                 action, env, projectname, flags, config, common_params)
    perform_start(base_dir, template_dir, project_dir, composer_base_command,
                  action, env, projectname, flags, config, common_params)


def perform_action(base_dir, template_dir, project_dir, composer_file,
                   composer_template_file, config_file, action, env, projectname,
                   flags, project_vars):
    """
    Perform desired action
    """
    composer_base_command = "docker-compose -p %s -f %s" % (projectname, composer_file,)
    current_user = pwd.getpwuid(os.getuid())
    user_uid = str(current_user.pw_uid)
    user_gid = str(current_user.pw_gid)
    docker_command_user_fix = "--user=%s:%s" % (
        user_uid, user_gid)
    if DEBUG:
        print("Composer base command: '%s'" % composer_base_command)
    with open(config_file, "r") as fd:
        config = json.loads(fd.read())
    common_params = {'template_dir': template_dir,
                     'project_dir': project_dir,
                     'project_name': projectname,
                     'composer_base_command': composer_base_command,
                     'docker_command_user_fix': docker_command_user_fix,
                     'user_uid': user_uid,
                     'user_gid': user_gid}
    common_params.update(project_vars)

    with open(composer_template_file, "r") as fd:
        composer_content = fd.read()
    with open(composer_file, "w") as fd:
        fd.write(composer_content % common_params)

    if action == "start":
        perform_start(base_dir, template_dir, project_dir, composer_base_command,
                      action, env, projectname, flags, config, common_params)
    elif action == "stop":
        perform_stop(base_dir, template_dir, project_dir, composer_base_command,
                     action, env, projectname, flags, config, common_params)
    elif action == "status":
        perform_status(base_dir, template_dir, project_dir, composer_base_command,
                       action, env, projectname, flags, config, common_params)
    elif action == "restart":
        perform_restart(base_dir, template_dir, project_dir, composer_base_command,
                        action, env, projectname, flags, config, common_params)


def parse_init(required=True):
    base_template_dir = os.path.join(
        utils.get_base_dir(__file__), TEMPLATE_DIRECTORY)
    available_templates = [item for item in os.listdir(
        base_template_dir) if os.path.isdir(os.path.join(base_template_dir, item))]

    parser = argparse.ArgumentParser(
        description='Create new system based on a template')
    parser.add_argument('--template', action="store",
                        choices=available_templates, required=required)
    parser.add_argument('--action', action="store",
                        choices=ACTIONS, required=True)
    parser.add_argument('--env', action="store", choices=ENVS, required=required)
    parser.add_argument('--flag', action="append",
                        help="Flags to be applied. Only steps with included "
                        "flags will be executed")
    parser.add_argument('--var', action="append",
                        help="Override default project vars. Each allowed var "
                        "is defined in its environment documentation. Format -> "
                        "varname:varvalue")
    parser.add_argument('--debug', action="store_true",
                        help="Add this argument to get extra verbosity on each "
                        "command")
    if required:
        parser.add_argument('projectname', action="store")
    else:
        parser.add_argument('projectname', action="store", nargs='?')
    return parser.parse_args()


def base_configuration(base_dir, templates_dir):
    """
    Parse configuration and update argsconf.json
    """
    global DEBUG
    args_conf_file = os.path.join(base_dir, "argsconf.json")

    if os.path.exists(args_conf_file):
        args = parse_init(required=False)
        with open(args_conf_file, "r") as fd:
            cacheargs = json.loads(fd.read())
        template = cacheargs.get("template") if not args.template else args.template
        action = cacheargs.get("action") if not args.action else args.action
        env = cacheargs.get("env") if not args.env else args.env
        projectname = cacheargs.get("projectname") if not args.projectname else args.projectname
        flags = cacheargs.get("flags") if not args.flag else args.flag
        DEBUG = cacheargs.get("debug") if not args.debug else args.debug
        uservars = cacheargs.get("uservars") if not args.var else args.var
    else:
        args = parse_init()
        template = args.template
        action = args.action
        env = args.env
        projectname = args.projectname
        flags = args.flag
        DEBUG = args.debug
        uservars = args.var

    with open(args_conf_file, "w") as fd:
        preserve_flags = os.path.join(templates_dir, template, env, "preserveflags.json")
        with open(preserve_flags, "r") as pffd:
            pflags = json.loads(pffd.read())
        fd.write(json.dumps({'template': template,
                             'action': action,
                             'env': env,
                             'projectname': projectname,
                             'flags': [flag for flag in flags if flag in pflags],
                             'uservars': uservars}))

    return template, action, env, projectname, flags, uservars


if __name__ == "__main__":
    base_dir = utils.get_base_dir(__file__)
    templates_dir = os.path.join(base_dir, TEMPLATE_DIRECTORY)

    template, action, env, projectname, flags, uservars = base_configuration(base_dir,
                                                                             templates_dir)

    if "new" in flags:
        ok = None
        while ok not in ["y", "n"]:
            ok = input('"New" flag can destroy several files as it creates structure. It can '
                       'lead to lose information. Do you want to continue? [y/n] ').lower()
        if ok == "n":
            exit(0)

    template_dir = os.path.join(templates_dir, template, env)
    project_dir = os.path.join(base_dir, PROJECT_DIRECTORY)
    composer_template_file = os.path.join(template_dir, DOCKER_COMPOSE_TEMPLATE_FILE)
    composer_file = os.path.join(template_dir, DOCKER_COMPOSE_FILE)
    config_file = os.path.join(template_dir, CONFIG_FILE)

    with open(os.path.join(template_dir, "defaultvars.json"), "r") as fd:
        pvars = json.loads(fd.read())

    if uservars:
        for uvar in uservars:
            key, val = uvar.split(":")
            pvars[key] = val

    perform_action(base_dir, template_dir, project_dir,
                   composer_file, composer_template_file, config_file,
                   action, env, projectname, flags, pvars)
