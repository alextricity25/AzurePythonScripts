"""
Author(s):
    Miguel Alex Cantu
Date: 02/21/2020
Description:
    This function will return a dictionary of all the
    credentialUserRegistrationDetails objects from the tenant indexed by 
    userPrincipalName
"""
#Imports
from make_request import paginate

# Variables
GRAPH_ENDPOINT = (
        "https://graph.microsoft.com/beta/reports/credentialUserRegistrationDetails")

def list_credential_user_registration_details(
        config,
        app):
    """
    TODO: Document parameters
    """
    user_registration_data = []
    retries = 0
    result = 0
    while retries < config["MAX_RETRIES"] and isinstance(result, int):
        result = paginate(GRAPH_ENDPOINT,
                   user_registration_data,
                   'value',
                   config,
                   app,
                   retry_count=retries)
        retries += 1

    # Converting returned data to a dictionary indexed by UPN
    user_registration_details = {}
    for user in user_reg_data:
        user_reg_details[user["userPrincipalName"]] = user
    return user_reg_details
