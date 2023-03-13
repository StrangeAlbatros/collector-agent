#!/usr/bin/env python3

""" Mac Collector """

from subprocess import check_output
from re import findall, compile, DOTALL
from json import dumps

P_LAUNCHCTL = r"([-\d]+)\t(\d+)\t(.+)"

class MacCollector:
    """ class Mac data Collector """
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
        # apple packages
        self.logger.debug("Debug: Get installed packages")
        self.installed_packages["pkgs"] = [ {
                    "name":elt,
                    "version": "unknown",
                    'architecture': "unknown",
                    "description": "unknown",
                } for elt in self.execute_command("pkgutil --pkgs").split("\n") ]
        # brew packages
        self.installed_packages["brew"] = [ {
                    "name":elt,
                    "version": "unknown",
                    'architecture': "unknown",
                    "description": "unknown",
                } for elt in self.execute_command("brew list").split("\n")]

    def get_services(self):
        """ Get services """
        # brew services
        self.logger.debug("Debug: Get services")
        brew_service = self.execute_command("brew services list")
        #TODO: know why brew services list return none services
        self.services["brew"] = brew_service.split("\n")
        self.services["launchctl"] = self.parse_launchctl(
            self.execute_command("launchctl list").split("\n")[1:]
        )

    def parse_launchctl(self, services):
        """ parse launchctl services """
        parsed_services = []
        for service in services:
            matches = findall(P_LAUNCHCTL, service)
            if matches:
                parsed_services.append({
                    "unit":matches[0][2],
                    "load": "unknown",
                    'active': "unknown",
                    "sub": "unknown",
                    "description": "unknown",
                })

        return parsed_services

    def execute_command(self, command):
        """ execute the command and retrieve its output """
        output = check_output(command, shell=True)
        return output.decode("utf-8")
