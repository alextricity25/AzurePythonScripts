"""
Author(s):
    Miguel Alex Cantu
Date: 04/13/2020
Description:
    This script generates a report of all the users in Azure,
    including their MFA registration status. The report will be
    dropped in /mfa_reports/csv.
"""
import argparse
import os
import msal
import logging
import json
import sys
from list_credential_user_registration_details import list_credential_user_registration_details
from list_all_users import list_all_users

# Configuring argument list
parser = argparse.ArgumentParser(
        usage='%(prog)s',
        formatter_class=argparse.RawTextHelpFormatter,
        description=("This script generates a report of all the users in Azure,"
                     "including their MFA registration status. The report will be"
                     "dropped in /mfa_reports/csv")
        )
parser.add_argument(
        '-s',
        '--smoke',
        action='store_true',
        required=False,
        help="Run a smoke test, without making API calls")
parsed_args = parser.parse_args()

# Prelimary checks

# Turn on logging
logging.basicConfig(level=logging.DEBUG)

# Variables
CONFIG_PATH = os.path.expanduser("~/.aut/aut_config.json")

# Get config for authenticating
## Ensure the config directory exists, if not, throw Exception
if not os.path.exists(CONFIG_PATH):
    raise Exception("Config not present in ~/.aut/aut_config.json")

config = json.load(open(CONFIG_PATH))

# Configuring MSAL app
# For more information on the MSAL Python library, visit:
# https://github.com/AzureAD/microsoft-authentication-library-for-python
app = msal.ConfidentialClientApplication(
        config["client_id"],
        authority=config["authority"],
        client_credential={
            "thumbprint": config["thumbprint"],
            "private_key": open(
                os.path.expanduser(config["private_key_file"])).read()})

# The meat of the program
#users_with_registration_details = list_credential_user_registration_details(config, app)
users_with_attributes = list_all_users(config, app)
