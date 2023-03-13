#!/usr/bin/env python3

""" Windows Collector """

from subprocess import check_output
from re import compile, MULTILINE
from json import dumps

class WindowsCollector:

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
        regex = compile(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(.*?)\s*$", MULTILINE)
        matches = regex.findall(self.execute_command(["powershell", "Get-Package"]))

        for match in matches:
            packages.append({
                'name': match[0],
                "version": match[1],
                'source': match[2],
                "provider": match[3],
            })
        print(dumps(packages, indent=4))
        self.installed_packages["packages"] = packages
        
    def get_services(self):
        """ Get services """
        pass
        
    def execute_command(self, command):
        """ Execute command """
        return check_output(command).decode()
    
if __name__ == "__main__":
    WindowsCollector({}, None)