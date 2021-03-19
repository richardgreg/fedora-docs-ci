# CI for Fedora Docs
Documentation on enabling continuous integration for the Fedora documentation website.

## Using the build script
### Requirements
`python3, podman, Apache server` 

### Cofigure the Apache server
* Install HTTPD packages.

    `sudo dnf install httpd -y`

* Start the HTTPD service.

    `sudo systemctl start httpd.service`

* (Optional) Add custom servername to /etc/hosts

### Create and activate a python virtual environment
`python3 -m venv venv`

`source venv/bin/activate`

`$ pip install -r requirements.txt.`

### Listen to and build PRs opened against Fedora Docs by running the consumer script
`$ python build-scripts/consumer.py`
