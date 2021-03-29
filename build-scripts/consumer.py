#!/usr/bin/env python3

from fedora_messaging.api import consume
from fedora_messaging.config import conf
from build import get_docs_builder, post_messenger


conf.setup_logging()


def print_message(message):
    """
    Print messages consumed by fedora messaging

    Args: a message object
    """
    print(message.topic)
    print(message._body['pullrequest'])


def build(message):
    """
    Build a pull request opened against fedora docs

    Args: a message object from Fedora Messages
    """
    if message.topic == "io.pagure.prod.pagure.pull-request.new":
        pr_data = message._body['pullrequest']
        if pr_data['project']['namespace'] == 'fedora-docs':
            get_docs_builder(pr_data)
            post_comment(pr_data)

    if message.topic == "io.pagure.prod.pagure.pull-request.rebased" or \
            message.topic == 'io.pagure.prod.pagure.pull-request.updated':
        pr_data = message._body['pullrequest']
        if pr_data['project']['namespace'] == 'fedora-docs':
            get_docs_builder(pr_data)

    

if __name__ == "__main__":
    conf.setup_logging()
    consume(build)
