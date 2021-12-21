import logging

import requests

from .models import SignedUrl, File

minizinc_data_name = "minizinc-app"
mzn_data_url = "http://"+minizinc_data_name+"/api/minizinc/upload"  # TODO Take as variable


def drop_file(body: str, user_id: str, computation_id: str):

    # Get upload-url
    headers = {'UserId': 'system', 'Role': 'admin'}
    response = requests.get(mzn_data_url, headers=headers)
    if response.status_code != 200:
        logging.error("minizinc-data replied {}".format(response.text))

    signed_url = SignedUrl.parse_raw(response.text)

    # upload solution
    response = requests.put(signed_url.url, data=body)
    if response.status_code != 200:
        logging.error("The S3-Bucket replied {}: {}".format(response.status_code, response.text))

    file_name = computation_id + ".txt"
    data = File(userID=user_id, fileUUID=signed_url.fileUUID, fileName=file_name)
    response = requests.post("http://"+minizinc_data_name+"/api/minizinc/upload", headers=headers, json=data.json())
    if response.status_code != 200:
        logging.error("minizinc-data replied {}: {}".format(response.status_code, response.text))

    return (signed_url.fileUUID, file_name)
