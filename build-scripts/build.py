#!/usr/bin/env python3

import os
import argparse
from git import Repo
import tempfile
import yaml
import requests
import shutil
from dotenv import load_dotenv


load_dotenv()

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

    # Check if a folder with the name intended for the PR build already exist.
    # delete if it does, else move built doc to the folder where apache will serve it
    if os.path.exists(f"/var/www/html/{pr_data['project']['name']}-pr{pr_data['id']}"):
        shutil.rmtree(f"/var/www/html/{pr_data['project']['name']}-pr{pr_data['id']}")
    try:
        shutil.move(f"{temp_dir.name + playbook_data['output']['dir'][1:]}",
                    f"/var/www/html/{pr_data['project']['name']}-pr{pr_data['id']}")
    except PermissionError:
        print("Operation not permitted.")
    # For other errors
    except shutil.Error as error:
        print(error)

    # Make sure folder is deleted after being cloned
    try:
        shutil.rmtree(temp_dir.name)
    except FileNotFoundError:
        print("File not found or already deleted")
    except PermissionError:
        print("Operation not permitted.")
    else:
        print("Temporary directory has been deleted")


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


def post_comment(pr_data):
    """
    Posts a comment under the PR with the link to the build

    Args: A dict object with information about a pull request
    """
    token = os.environ.get("api-key")
    API_KEY = token
    API_ENDPOINT = f"https://pagure.io/api/0/{pr_data['full_url'][18:]}/comment"

    comment = f"Thank you for your contribution. Use the following link to see a \
preview of your contribution.\nDNS/{pr_data['project']['name']}-pr{pr_data['id']}. \
Do keep in mind that the build gets deleted if there is no update for more than a \
period of 2 weeks."

    data = {
        'comment': comment
    }

    headers = {'Authorization': f'token {API_KEY}'}

    requests.post(url=API_ENDPOINT, data=data, headers=headers)


if __name__ == "__main__":
    pr_data = get_data()
    get_docs_builder(pr_data)
