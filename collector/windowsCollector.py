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

        regex = compile(r"^(.{30})\s(.{16})\s(.{32})\s(\S*)", MULTILINE)
        matches = regex.findall(self.execute_command(["powershell", "Get-Package"]))

        for match in matches:
            packages.append({
                'name': self.trim_str(match[0]),
                "version": self.trim_str(match[1]),
                'source': self.trim_str(match[2]),
                "provider": self.trim_str(match[3]),
            })
        self.installed_packages["packages"] = packages[2:]
        
    def get_services(self):
        """ Get services """
        output_lines = self.execute_command("sc queryex type=service").split('\n')
        services = []

        for i in range(len(output_lines)):
            if 'SERVICE_NAME' in output_lines[i]:
                services.append({
                    'unit':output_lines[i].split(': ')[1].strip(),
                    "load": "unknown",
                    'active': "unknown",
                    "sub": "unknown",
                    "description": "unknown",
                })

        self.services["queyex"] = services
        
    def execute_command(self, command):
        """ Execute command """
        return check_output(command).decode("iso-8859-1")
    
    def trim_str(self, data):
        """ trim string """
        if not isinstance(data, str):
            return data
        tmp = data.replace("  ","").replace('...', '')
        return tmp if tmp else "unknown"
    
if __name__ == "__main__":
    WindowsCollector({}, None)