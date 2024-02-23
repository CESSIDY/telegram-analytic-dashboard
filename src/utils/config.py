import configparser
import os
import logging


def get_configurations() -> dict:
    config_file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), '..', '..', '..', "config.ini"))
    config = configparser.ConfigParser()
    config.read(config_file_path)

    return config


def get_proxy_configurations() -> dict:
    proxy = {}
    config = get_configurations()
    is_proxy_enabled = int(config['Proxy']['proxy_enabled'])

    if is_proxy_enabled:
        proxy = {
            'proxy_type': config['Proxy']['proxy_type'],  # (mandatory) protocol to use
            'addr': config['Proxy']['addr'],  # (mandatory) proxy IP address
            'port': config['Proxy']['port'],  # (mandatory) proxy port number
            'username': config['Proxy']['username'],  # (optional) username if the proxy requires auth
            'password': config['Proxy']['password'],  # (optional) password if the proxy requires auth
            'rdns': True  # (optional) whether to use remote or local resolve, default remote
        }
    return proxy


def configure_logging(name="telegram_commentator"):
    logging.basicConfig(filename=f"{name}.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO)
