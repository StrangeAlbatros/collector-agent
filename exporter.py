#!/usr/bin/env python3

""" Data Exporter"""

from requests import Session
from requests.exceptions import SSLError
from json import dumps

class DataExporter:
    """ class Data Exporter """
    def __init__(self, kwargs, logger) -> None:
        self.logger = logger
        self.session = Session()
        self.url = kwargs.get('host') + ":" + str(kwargs.get('port')) + kwargs.get('url', '')
        self.session.headers.update({'Content-Type': 'application/json'})

        if kwargs.get('verify', False):
            self.session.verify = kwargs.get('verify')
        if kwargs.get('cert', False):
            self.session.cert = kwargs.get('cert')

    def send_data(self, data):
        """ Send data to the server """
        try:
            response = self.session.post(
                self.url,
                data=dumps(data),
            )
            if response.status_code != 200:
                print('Error: ' + response.text)
                self.logger.warning('Warning: ' + response.text)
            else:
                self.logger.info('Data sent')
        except SSLError as e:
            print('Error SSL: ' + str(e))
            self.logger.error('Error: ' + str(e))
        except Exception as e:
            print('Error: ' + str(e))
            self.logger.error('Error: ' + str(e))