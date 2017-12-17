# -*- coding: utf-8 -*-
"""
Systems commander main script
"""
import argparse
import subprocess

BASE_COMMAND = "docker exec %s %s"


def run_command(containername, command):
    """
    Run command
    """
    cmd = BASE_COMMAND % (containername, command)
    subprocess.run(cmd.split())


def parse_init():
    """
    Parse basic params
    """
    parser = argparse.ArgumentParser(
        description='Run a command into a docker container')
    parser.add_argument('containername', action="store")
    parser.add_argument('command', action="store")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_init()
    run_command(args.containername, args.command)
