import logging

import requests

from .models import SignedUrl

mzn_data_url = "http://minizinc-app/api/minizinc/upload"  # TODO Take as variable


def drop_file(body: str):

    # Get upload-url
    headers = {'UserId': 'system', 'Role': 'admin'}
    response = requests.get(mzn_data_url, headers=headers)
    if response.status_code != 200:
        logging.error("minizinc-data replied {}".format(response.text))

    signed_url = SignedUrl.parse_raw(response.text)

    # upload solution
    response = requests.put(signed_url.url, data=body)
    if response.status_code != 200:
        logging.error("minizinc-data replied {}: {}".format(response.status_code, response.text))

    return (signed_url.url, signed_url.fileUUID)
