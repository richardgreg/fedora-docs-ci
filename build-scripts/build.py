#!/usr/bin/env python3

import os
import argparse
from git import Repo
import http.server
import socketserver
import tempfile
import yaml
import requests


class Handler(http.server.SimpleHTTPRequestHandler):
    """
    Custom class definition for simple http server
    Used for testing built docs in development
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


# Port and directory to serve the built files
PORT = 8000
DIRECTORY = 'public'
handler = Handler

DOCS_BUILDER_URL = "https://pagure.io/fedora-docs/docs-fp-o.git"
DOCS_BUILDER_BRANCH = 'prod'
PAGURE = 'https://pagure.io/'


def get_data():
    """
    Use the argparse library to provide a user friendly cli.
    Argsparse asks for a Pagure API containing info relating to a pull request

    Returns:
        Data needed to build the docs site with with the new edit
    """
    parser = argparse.ArgumentParser(description='Get the data for a particular for \
                                    a pull request related to a doc section.')
    parser.add_argument("pull_request_api", help="Pagure API containing information \
                        relating to a pull request")

    args = parser.parse_args()

    response = requests.get(f'{args.pull_request_api}')
    pr_data = response.json()
    return pr_data


def get_docs_builder(pr_data):
    """
    Gets the fedora docs-fp-o used for building the entire docs site

    Args: A dict object with information about a pull request
    """
    # Temporary directory to store the docs builder for preview in /tmp folder
    temp_dir = tempfile.TemporaryDirectory(prefix="docs-ci-%s-" % pr_data['id'],
                                           dir='/tmp')

    # Use git library to clone docs-fp-o and branch into a temporary
    Repo.clone_from(url=DOCS_BUILDER_URL, to_path=f'{temp_dir.name}',
                    branch=DOCS_BUILDER_BRANCH)

    # Change directory into the folder.
    # Only way for the script to recognise site.yml
    os.chdir(f'{temp_dir.name}')

    # Build the docs site with the data from the PR. Returns the playbook
    # data from site.yml This is used when writing to Apache config
    playbook_data = build_docs(pr_data)

    # Write Apache configurations
    write_apache_configurations(pr_data, playbook_data, temp_dir)


def build_docs(pr_data):
    """
    Load the data from site.yml as a dict and append a fork of the
    docs_repo to the list of sites to be built
    """
    with open('site.yml') as f:
        playbook_data = yaml.load(f, Loader=yaml.SafeLoader)

    sources = playbook_data['content']['sources']
    # Iterate through the sources and replace the docs upstream with the fork
    for i in range(len(sources)):
        if sources[i]['url'] == pr_data['project']['full_url']+'.git':
            sources[i]['url'] = PAGURE + pr_data['repo_from']['fullname']+'.git'
            # Antora builds 'master' branch by default, so if it's not master
            # branch declare it in the playbook
            if pr_data['branch_from'] != 'master':
                if 'branches' in sources[i]:
                    # Sometimes it's a list of branches
                    if type(sources[i]['branches']) == list:
                        sources[i]['branches'].append(pr_data['branch_from'])
                else:
                    sources[i]['branches'] = pr_data['branch_from']

    with open('site.yml', 'w') as f:
        yaml.dump(playbook_data, f)

    os.system("./build.sh")

    return playbook_data


def write_apache_configurations(pr_data, playbook_data, temp_dir):
    """
    Write apache configuration for the built site

    Args:
        A dict object containing information about a pull request
        Antora playbook data as a dict object
        The temporary directory containing the docs builder
    """
    # Open the custom apache configuration and add the document root
    # and server name to the file
    with open('/etc/httpd/conf.d/myconf.conf', 'a+') as f:
	    f.write(f"""
            <VirtualHost *:80>
                DocumentRoot {temp_dir.name + playbook_data['output']['dir'][1:]}
                ServerName fedoradocs.pr{pr_data['id']}.com
            </VirtualHost>""")

    # Open the system host file and add the custom host name to the list
    with open('/etc/hosts', 'a+') as f:
        f.write(f"""127.0.0.1  fedoradocs.pr{pr_data['id']}.com""")


def serve_docs():
    """
    A simple http server to serve file
    """
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Server started at 0.0.0.0:" + str(PORT))
        httpd.serve_forever()


if __name__ == "__main__":
    pr_data = get_data()
    get_docs_builder(pr_data)
