"""
Author(s):
    Miguel Alex Cantu
Date: 04/20/2020
Description:
    This script contains a function called paginate,
    which makes a requests and pages through the 
    results recursively. It uses the cached access
    token to make subsequent requests to the graph
    API.
"""
# Imports
import logging
import requests
import time

def paginate(endpoint,
             return_data,
             key,
             config,
             app,
             parsed_args,
             transformer=None,
             test_data=None,
             std_output=True,
             payload={},
             throttle=0,
             retry_count=0):
    """
    TODO:
    Document parameters
    """
    # If test_data is provided, then do not make the API call
    if test_data and parsed_args.smoke:
        graph_data = test_data
    else:
        # If test_data is not given, assume normal operation and make
        # the API requests

        # Checking to see if token is in cache. For documentation on this
        # operation, please see:
        # https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/dev/sample/confidential_client_certificate_sample.py#L57
        result = app.acquire_token_silent(config["scope"], account=None)
        if not result:
            logging.info(
                    "No suitable token exists in cache. Let's get a new one"
                    " from AAD")
            result = app.acquire_token_for_client(scopes=config["scope"])

        if "access_token" in result:
            logging.info("Retry count is {}".format(retry_count))
            # If there is payload, then make a post request to the endpoint
            if payload:
                # TODO: IMPLEMENT make_post_request
                print("post requests not implemented yet")
                exit()
                graph_data_response = make_post_request(endpoint, result)
            else:
                # TODO: Implement make_get_request
                graph_data_response = make_get_request(endpoint, result)

        graph_data = graph_data_response.json()

        # If status code is not 200, then return status code
        if graph_data_response.status_code != 200:
            return graph_data_response.status_code

        # TODO: Transformations should now happen outside of this function

    # Shove the data returned from the endpoint into the data variable
    if key == '':
        return_data.append(graph_data)
    else:
        return_data.extend(graph_data.get(key, ""))

    # Recursively follow nextLink
    # For more information on paging with MS Graph, see:
    # https://docs.microsoft.com/en-us/graph/paging
    if graph_data.get("@odata.nextLink", ""):
        time.sleep(throttle)
        return paginate(
                   graph_data["@odata.nextLink"],
                   return_data,
                   key,
                   config,
                   app,
                   parsed_args,
                   transformer=transformer,
                   test_data=test_data,
                   std_output=std_output,
                   payload=payload,
                   throttle=throttle,
                   retry_count=retry_count)

    return return_data

def make_get_request(endpoint, result):
    """
    This function makes a get request to the given endpoint using the access
    token provided by `result`
    TODO: Document parameters
    """
    response = requests.get(
            endpoint,
            headers={
                "Authorization": "Bearer " + result["access_token"],
                "Content-Type": "application/json"
            })
    return response
