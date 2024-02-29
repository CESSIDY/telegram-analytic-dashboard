import logging

from . import settings


def get_proxy_configurations() -> dict:
    proxy = {}

    if settings.PROXY_ENABLED:
        proxy = {
            'proxy_type': settings.PROXY_TYPE,  # (mandatory) protocol to use
            'addr': settings.PROXY_ADDRESS,  # (mandatory) proxy IP address
            'port': settings.PROXY_PORT,  # (mandatory) proxy port number
            'username': settings.PROXY_USERNAME,  # (optional) username if the proxy requires auth
            'password': settings.PROXY_PASSWORD,  # (optional) password if the proxy requires auth
            'rdns': True  # (optional) whether to use remote or local resolve, default remote
        }
    return proxy


def configure_logging(name="telegram_commentator"):
    logging.basicConfig(filename=f"{name}.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.INFO,
                        encoding='UTF-8')
