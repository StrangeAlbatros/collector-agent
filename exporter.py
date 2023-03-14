#!/usr/bin/env python3

""" Data Exporter"""

from requests import post, Session
from json import dumps

class DataExporter:
    """ class Data Exporter """
    def __init__(self, kwargs, logger) -> None:
        self.logger = logger
        self.url = kwargs.get('host') + ":" + str(kwargs.get('port')) + kwargs.get('url', '')
        self.headers = {'Content-Type': 'application/json'}
        self.verify = kwargs.get('verify', False)

    def send_data(self, data):
        """ Send data to the server """
        try:
            response = post(
                self.url,
                data=dumps(data),
                headers=self.headers,
                verify=self.verify
            )
            if response.status_code != 200:
                print('Error: ' + response.text)
                self.logger.warning('Warning: ' + response.text)
            else:
                self.logger.info('Data sent')
        except Exception as e:
            print('Error: ' + str(e))
            self.logger.error('Error: ' + str(e))