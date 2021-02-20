#!/usr/bin/env python3

import os
import argparse
from git import Repo
import http.server
import socketserver
import tempfile
import yaml
import requests


# Custom class definition for simple http server
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


# Temporary directory (Store file in /tmp for production)
temp_dir = tempfile.TemporaryDirectory(dir="./")

# Port and directory to serve the built files
PORT = 8000
DIRECTORY = 'public'
handler = Handler

DOCS_BUILDER = "https://pagure.io/fedora-docs/docs-fp-o.git"
DOCS_BUILDER_BRANCH = 'prod'
PAGURE = 'https://pagure.io/'

# Use the argparse library to provide user friendly cli
parser = argparse.ArgumentParser(description='Get the data for a particular for \
                                 a pull request related to a doc section.')
parser.add_argument("pull_request_api", help="Pagure API containing information \
                    relating to a pull request")

args = parser.parse_args()

response = requests.get(f'{args.pull_request_api}')
pr_data = response.json()

# Use git library to clone docs-fp-o and branch into a temporary
Repo.clone_from(DOCS_BUILDER, f'./{temp_dir.name}',
                branch=DOCS_BUILDER_BRANCH)

os.chdir(f'./{temp_dir.name}')

# Load the data from site.yml as a dict and append a fork of the
# docs_repo to the list of sites to be built
with open('site.yml',) as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

sources = data['content']['sources']
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
    yaml.dump(data, f)

os.system("./build.sh")

# A simple http server to serve file
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Server started at 0.0.0.0:" + str(PORT))
    httpd.serve_forever()
