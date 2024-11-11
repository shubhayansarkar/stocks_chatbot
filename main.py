import yaml
import logging.config


if __name__ == "__main__":
    with open('logger-config.yml', 'r') as cfg:
        logging.config.dictConfig(yaml.load(cfg, yaml.SafeLoader))
        logger = logging.getLogger('devlog')
        logger.info('loaded logger')