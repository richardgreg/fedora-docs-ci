from fedora_messaging import api, config

config.conf.setup_logging()
api.publish(api.Message(topic="hello", body={"Hello": "world!"}))
