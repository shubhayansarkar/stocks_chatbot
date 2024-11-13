import logging.config

import yaml

LOGGING_CONFIG_FILE = "logger-config.yml"

with open(LOGGING_CONFIG_FILE, 'r') as cfg:
    logging.config.dictConfig(yaml.load(cfg, yaml.SafeLoader))
    logger = logging.getLogger('devlog')
    logger.debug('[OK] logger is loaded')