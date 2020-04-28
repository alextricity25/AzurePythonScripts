"""
Author(s):
    Miguel Alex Cantu
Date: 04/13/2020
Description:
    Send an email, using the graph API, to a recipient
"""

import os
import msal
import logging
import json
import sys

# Prelimary checks
# Check argument is given
if len(sys.argv.length) < 2:
    raise Exception("Must give an email as second argument!")

logging.basicConfig(level=logging.DEBUG)

# Variables
CONFIG_PATH = os.path.expanduser("~/.aut/aut_config.json")
EMAIL_FROM = sys.argv[1]
GRAPH_ENDPOINT = f"https://graph.microsoft.com/v1.0/users/{EMAIL_FROM}/sendMail"


# Get config for authenticating
## Ensure the config directory exists, if not, throw Exception
if not os.path.exists(CONFIG_PATH):
    raise Exception("Config not present in ~/.aut/aut_config.json")

config = json.load(open(CONFIG_PATH))

# Configuring MSAL app
app = msal.ConfidentialClientApplication(
        config["client_id"],
        authority=config["authority"],
        client_credential={
            "thumbprint": config["thumbprint"],
            "private_key": open(
                os.path.expanduser(config["private_key_file"])).read()})



