"""
Author(s):
    Miguel Alex Cantu
Date: 04/21/2020
Description:
    This function will return a dictionary of all the users
    in the tenant, indexed by userPrincipalName
"""
# Imports
from make_request import paginate

# Variables
# This query fetches all of the users along with the attributes defined
# in the select filter
GRAPH_ENDPOINT = (
        "https://graph.microsoft.com/v1.0"
        "/users"
        "?$select="
        "accountEnabled,"
        "companyName,"
        "country,"
        "createdDateTime,"
        "displayName,"
        "id,"
        "jobTitle,"
        "mail,"
        "officeLocation,"
        "onPremisesExtensionAttributes,"
        "onPremisesSamAccountName,"
        "usageLocation,"
        "userPrincipalName,")

def list_all_users(config, app):
    user_data = []
    paginate(GRAPH_ENDPOINT,
             user_data,
             'value',
             config,
             app)
    
    # Converting data to dictionary indexed by UPN
    users = {}
    for user in user_data:
        users[user["userPrincipalName"]] = user

    return users
