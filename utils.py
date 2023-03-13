#!/usr/bin/env python3

import logging

from os.path import exists, isfile, join
from pathlib import Path
from os import mkdir, W_OK, access
from logging.handlers import TimedRotatingFileHandler

from yaml import safe_load
from yaml import YAMLError


def create_logger(kwargs):

    path = kwargs.get('log.path', '/var/log/collector-agent')
    name = kwargs.get('log.name', 'collector-agent')

    if not exists(path):
        try:
            mkdir(path)
        except PermissionError:
            print('Error: No write access to {0}'.format(path))
            print('Log file will be created in home directory')
            path = join(Path.home(), 'collector-agent')
            if not exists(path):
                mkdir(path)

    if not access(path, W_OK):
        print('Error: No write access to {0}'.format(path))
        print('Log file will be created in home directory')
        path = join(Path.home(), 'collector-agent')
        if not exists(path):
            mkdir(path)

    logger_formatter = logging.Formatter(
        '%(asctime)s [%(name)s] : %(levelname)s %(message)s',
        datefmt='%B. %d %H:%M:'
    )
    logger = logging.getLogger(name)
    handler_logger = logging.handlers.TimedRotatingFileHandler(
        join(path, name ) + ".log",
        when="D",
        interval=1,
        encoding="utf-8",
        backupCount=30
    )

    handler_logger.setFormatter(logger_formatter)
    logger.addHandler(handler_logger)

    if kwargs.get('log.debug', True):
        logger.setLevel(logging.DEBUG)

    return logger

def load_conf(filepath='conf.yml'):
    ext = Path(filepath).suffix
    if ext == '.yml':
        return load_yml(filepath)
    else:
        raise Exception('Configuration file must be a YAML file (.yml)')

def load_yml(filepath):
    """ Function wich import parameter of congi file """
    if not exists(filepath) or not isfile(filepath):
        raise FileNotFoundError('Configuration file not found: {0}'.format(filepath))

    with open(filepath, 'r', encoding='utf8') as stream:
        try:
            conf = safe_load(stream)
        except YAMLError:
            raise Exception('Error in reading file: {0}'.format(filepath))
    
    return conf