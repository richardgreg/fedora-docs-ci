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

* Configure Fedora Messaging public broker. Responsible for listening to activities on on doc repos.

    [Fedora Public Broker](https://fedora-messaging.readthedocs.io/en/stable/quick-start.html#fedora-s-public-broker)

### Create and activate a python virtual environment
`python3 -m venv venv`

`source venv/bin/activate`

`$ pip install -r requirements.txt.`

`touch .env`

In the command below replace `<your-api-key>` with the api token of a user
responsible for notifying contributors about their PR

`echo "api-key = '<your-api-key>'" > .env`

### Listen to and build PRs opened against Fedora Docs by running the consumer script
`$ python build-scripts/consumer.py`
