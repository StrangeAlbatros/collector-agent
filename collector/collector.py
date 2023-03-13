#!/usr/bin/env python3

""" Collector """

NETWORK_USE = True
try:
    import netifaces
except ImportError:
    NETWORK_USE = False
    print('Warning: netifaces not found, network information will not be collected')

import platform
import sys
from json import dumps

from collector.linuxCollector import LinuxCollector
from collector.macCollector import MacCollector
from collector.windowsCollector import WindowsCollector

class Collector:
    """ class Collector """
    def __init__(self, kwargs, logger) -> None:
        self.informations = {}
        self.logger = logger

        self.get_information()
        self.logger.debug('Debug: ' + dumps(self.informations))
        self.run_collector(kwargs)
        self.logger.info('Collector done')

    def run_collector(self, kwargs):
        """ run collector """
        self.logger.debug('Debug: Run collector')

        if self.informations['os']['name'].lower().startswith('linux'):
            self.collector = LinuxCollector(kwargs, self.logger)
        elif self.informations['os']['name'].lower().startswith('win'):
            self.collector = WindowsCollector(kwargs, self.logger)
        elif self.informations['os']['name'].lower().startswith('darwin'):
            self.collector = MacCollector(kwargs, self.logger)
        else:
            raise Exception('Unsupported OS')

    def get_information(self):
        """ get information """
        self.informations['os'] = {
            'name': platform.system(),
            'version': platform.release(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
        }
        if NETWORK_USE:
            self.get_interfaces()
        else:
            self.informations['network'] = {}

    def add_information(self, key, value):
        """ add information """
        try:
            self.informations[key] = value
        except KeyError:
            self.logger.error(
                'Error: Key not found ({0}) in informations'.format(key)
            )

    def get_interfaces(self):
        """ get network interfaces """
        interfaces = {}

        for interface in netifaces.interfaces():
            for num in netifaces.ifaddresses(interface):
                    interfaces[interface] = netifaces.ifaddresses(interface)[num]
        self.informations['network'] = interfaces

    def get_data(self):
        """ get data """
        return {
            "informations":self.informations['os'],
            "network":self.informations['network'],
            "packages":self.collector.installed_packages,
            "services":self.collector.services,
        }
