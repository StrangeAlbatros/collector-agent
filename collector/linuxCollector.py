#!/usr/bin/env python3

""" Linux Collector """

from subprocess import check_output
from re import findall, compile, MULTILINE

class LinuxCollector:
    """ class Linux data Collector """
    def __init__(self, kwargs, logger):
        self.installed_packages = {}
        self.services = {}
        self.logger = logger

        if kwargs.get("supervision.packages", True):
            self.get_installed_packages()
        if kwargs.get("supervision.services", True):
            self.get_services()

    def get_installed_packages(self):
        """ Get installed packages """
        self.logger.debug("Debug: Get installed packages")
        packages = []
        # linux packages
        regex = compile(r"^ii\s+(\S+)\s+(\S+)\s+(.*)$", MULTILINE)
        matches = regex.findall(self.execute_command("dpkg -l"))

        for match in matches:
            packages.append({
                'name': match[0],
                "version": match[1],
                'architecture': match[2],
                "description": match[3],
            })
        self.installed_packages["dpkg"] = packages

    def get_services(self):
        """ Get services """
        self.logger.debug("Debug: Get services")
        output = self.execute_command("systemctl --type=service --state=running")
        pattern = r"(\S+)\s+(\S+)\s+(\S+)\s+\S+\s+(\S+)\s+(.+)"
        services = []
        for service in output.split("\n")[1:-5]:
            matches = findall(pattern, service)
            if matches:
                services.append({
                    'unit': matches[0][0],
                    "load": matches[0][1],
                    'active': matches[0][2],
                    "sub": matches[0][3],
                    "description": matches[0][4],
                })
        self.services["systemctl"] = services

    def execute_command(self, command):
        """ execute the command and retrieve its output """
        output = check_output(command, shell=True)
        return output.decode("utf-8")
