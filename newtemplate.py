# -*- coding: utf-8 -*-
"""
Utility to create scaffold for new templates
"""
import argparse
import os
import subprocess
import utils

DEBUG = False


def parse_init():
    parser = argparse.ArgumentParser(description='Create new template scaffold')
    parser.add_argument('--debug', action="store_true",
                        help="Add this argument to get extra verbosity on each command")
    parser.add_argument('templatename', action="store")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_init()
    templatename = args.templatename
    DEBUG = args.debug
    base_dir = utils.get_base_dir(__file__)
    template_dir = os.path.join(base_dir, "templates", templatename)
    if os.path.exists(template_dir):
        print("Template exists. Aborting")
        exit(0)
    for command in [
            "mkdir -p %s" % template_dir,
            "mkdir -p %s/dev" % template_dir,
            "mkdir -p %s/prod" % template_dir,
            "touch %s/README.md" % template_dir,
            "touch %s/dev/README.md" % template_dir,
            "touch %s/prod/README.md" % template_dir,
            "touch %s/dev/docker-compose.yml.template" % template_dir,
            "touch %s/prod/docker-compose.yml.template" % template_dir,
            "touch %s/dev/defaultvars.json" % template_dir,
            "touch %s/prod/defaultvars.json" % template_dir,
            "touch %s/dev/builderconfig.json" % template_dir,
            "touch %s/prod/builderconfig.json" % template_dir,
    ]:
        if DEBUG:
            print("Executing '%s'" % command)
            subprocess.run(command.split())
