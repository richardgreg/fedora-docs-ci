from fedora_messaging import api, config

config.conf.setup_logging()
api.consume(lambda message: print(message))
