#!/usr/bin/env python3

import os
import argparse
from git import Repo
import http.server
import socketserver
import tempfile
import yaml


# Custom class definition for simple http server
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


# Temporary directory
temp_dir = tempfile.TemporaryDirectory(dir="./")

# Port and directory to serve the built files
PORT = 8000
DIRECTORY = 'public'
handler = Handler


# Use the argparse library to provide user friendly cli
parser = argparse.ArgumentParser(description='Get the url of the git \
                                 repository of the Fedora docs builder and \
                                 the docs setcion.')
parser.add_argument("docs_fp_o", help="Git URL of the Fedora Documentation \
                    Website Builder")
parser.add_argument("docs_fp_o_branch", help="The branch of the Fedora \
                    Documentation Website Builder")
parser.add_argument("docs_repo", help="The git repository of the content\
                    to be built by docs-fpo")
parser.add_argument("docs_repo_branch", help="The branch of the git repository\
                    to be cloned")

args = parser.parse_args()

# Use git library to clone docs-fp-o and branch into a temporary
Repo.clone_from(args.docs_fp_o, f'./{temp_dir.name}',
                branch=args.docs_fp_o_branch)

os.chdir(f'./{temp_dir.name}')

# Load the data from site.yml as a dict and append docs_repo to the list of
# sites to be built
with open('site.yml',) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

data['content']['sources'].append({'url': f'{args.docs_repo}',
                                  'branches': f'{args.docs_repo_branch}'})

# Load the file back into site.yml
with open('site.yml', 'w') as f:
    yaml.dump(data, f)

os.system("./build.sh")

# A simple http server to serve file
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Server started at localhost:" + str(PORT))
    httpd.serve_forever()
