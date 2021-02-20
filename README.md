# CI for Fedora Docs
Information on enabling continuous integration for the Fedora documentation website.

## Using the build script
### Requirements
`python3, podman`

### Create and activate a python virtual environment
`python3 -m venv venv`
`source venv/bin/activate`
`$ pip install -r requirements.txt.`

### Build and preview the the docs repo with the build script
`$ python build.py <pagure_pr_api>`

Visit 0.0.0.0:8000/ to preview site
