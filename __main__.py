#!/usr/bin/env python3

from argparse import ArgumentParser

from json import dumps

from exporter import DataExporter
from collector.collector import Collector
from utils import create_logger, load_conf

def main(args):

    if args.config_file:
        conf = load_conf(args.config_file)
    else:
        conf = load_conf()

    logger = create_logger(conf)
    collector = Collector(conf, logger)
    if not conf.get('server'):
        raise Exception('No server configuration found')

    exporter = DataExporter(conf.get('server'), logger)
    exporter.send_data(collector.get_data())

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c', '--config-file',
        help='Path to the config file',
        default=None
    )
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
