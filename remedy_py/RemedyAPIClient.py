# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Brian Reid
# MIT License
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# pragma pylint: disable=unused-argument, no-self-use, undefined-variable


# Changelog
###############################################################################
# When       # Who                    # What
###############################################################################
# 2023 01 08 # Daniel Companeetz      # Attachments and worklogs to incidents

import requests
from .interface.remedy_api import RemedyAPI
# Load constant values for API Calls
from .RemedyConstants import *
from os import sep, SEEK_END
from os.path import getsize
import json

REQUEST_PREFIX = "/arsys/v1/entry"
DEFAULT_TIMEOUT = 30

class RemedyClient(RemedyAPI):

    def __init__(self, host, username, password, port=None, verify=True, proxies={}, timeout=DEFAULT_TIMEOUT):
        self.host = host
        self.username = username
        self.password = password
        self.verify = verify
        self.proxies = proxies
        self.timeout = timeout
        self.port = port or DEFAULT_HTTPS_PORT if self.verify else port or DEFAULT_HTTP_PORT
        self.base_url = HTTPS_BASE_URL(self.host, self.port) if self.verify else HTTP_BASE_URL(self.host, self.port)
        self.authHeaders = {"content-type": "application/x-www-form-urlencoded"}
        self.isLoggedin = False
        self.reqHeaders = self.build_request_headers()

    def get_token(self):
        """
        Accesses the Remedy simple authentication endpoint
        to retrieve a JWT authorization token. The token is
        decoded based on the apparent_encoding.

        :return: the token
        :rtype: str
        """
        url = self.base_url + "/jwt/login"
        data = {"username": self.username, "password": self.password}

        response = requests.request("POST", url, data=data, headers=self.authHeaders, 
                                    verify=self.verify, proxies=self.proxies, timeout=self.timeout)
        response.raise_for_status()
        token = response.content
        encoding = response.apparent_encoding
        token = token.decode(encoding)

        self.isLoggedin = True

        return token

    def build_request_headers(self, new_headers = None ):
        """
        Builds the request headers that Remedy expects
        for calls to the REST API

        :return: dict of request headers
        :rtype: dict
        """

        if not self.isLoggedin:
            token = self.get_token()

        reqHeaders = {
            "Authorization": "AR-JWT " + token
        }

        # override default and add new headers as needed
        if new_headers is not None:
            for key in new_headers.keys():
                reqHeaders[key.lower()] = new_headers[key] 

        no_content_type = True
        for key in reqHeaders.keys():
            if 'content-type' == key.lower():
                no_content_type = False
        
        if no_content_type:
            reqHeaders['content-type'] = 'application/json'

        return reqHeaders

    def release_token(self):
        """
        Releases a JWT token so that it cannot be used
        for further interaction with the REST API.
        The function returns: a tuple with the response content as json and the http status code.

        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        url = self.base_url + "/jwt/logout"

        response = requests.request("POST", url, headers=self.reqHeaders, verify=self.verify,
                                    proxies=self.proxies, timeout=self.timeout)
        response.raise_for_status()

        # logging off returns an empty 204
        # return empty json in the absence of response/incident content
        response_json = response.json() if response.content else {}

        self.isLoggedin = False

        return response_json, response.status_code

    def create_form_entry(self, form_name, values, headers=None, return_values=[], timeout=None, payload={}):
        """
        create_form_entry is a member function used to take a payload
        and form name and use it to create a new entry on the Remedy system. 
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to add an entry for
        :type form_name: str
        :param values: dictionary of incident values
        :type values: dict
        :param return_values: list of field names to return from the created entry
        :type return_values: list
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :type payload: dict, optional
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        if len(return_values) == 0:
            field_list = ["Incident Number"]
        else:
            field_list = ', '.join(return_values)
        url = self.base_url + REQUEST_PREFIX + "/{}?fields=values({})".format(form_name, field_list)

        if headers is None:
            reqHeaders = self.reqHeaders
        else:
            reqHeaders = self.build_request_headers(headers)

        if timeout is None:
            timeout = self.timeout

        entry = { "values": values}

        response = requests.request("POST", url, json=entry, headers=reqHeaders, verify=self.verify,
                            proxies=self.proxies, timeout=timeout)
            
        response.raise_for_status()
        
        return response.json(), response.status_code

    def get_form_entry(self, form_name, req_id, payload={}):
        """
        get_form_entry is a member function used to gather form data
        based on a form name and request ID
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :type form_name: str
        :param req_id: the request ID of the desired entry
        :type req_id: str
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :type payload: dict, optional
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        url = self.base_url + REQUEST_PREFIX + "/{}/{}".format(form_name, req_id)
        response = requests.request("GET", url, headers=self.reqHeaders, verify=self.verify,
                                    proxies=self.proxies, timeout=self.timeout)
        response.raise_for_status()                                    

        return response.json(), response.status_code

    def update_form_entry(self, form_name, req_id, values, payload={}):
        """
        update_form_entry is a member function used to update form data
        based on a form name and request ID
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :type form_name: str
        :param req_id: the request ID of the desired entry
        :type req_id: str
        :param values: dict of incident values to update
        :type values: dict
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :type payload: dict, optional
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        entry = {
            "values": values
        }
        url = self.base_url + REQUEST_PREFIX + "/{}/{}".format(form_name, req_id)

        response = requests.request("PUT", url, json=entry, headers=self.reqHeaders, verify=self.verify,
                                    proxies=self.proxies, timeout=self.timeout)
        response.raise_for_status()
        
        # Remedy returns an empty 204 for form updates.
        # get the updated incident and return it with the update status code
        status_code = response.status_code
        updated_incident, _ = self.get_form_entry(form_name, req_id, values)

        return updated_incident, status_code

    def delete_form_entry(self, form_name, req_id, payload={}):
        """
        delete_form_entry is a member function used to delete
        a form entry based on a form name and request ID.
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :type form_name: str
        :param req_id: the request ID of the desired entry
        :type req_id: str
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :type payload: dict, optional
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        url = self.base_url + REQUEST_PREFIX + "/{}/{}".format(form_name, req_id)
        response = requests.request("DELETE", url, headers=self.reqHeaders, verify=self.verify,
                                    proxies=self.proxies, timeout=self.timeout)
        response.raise_for_status()

        response_json = response.json() if response.content else {}

        # Remedy returns an empty 204 for form deletion.
        # return empty json in the absence of response/incident content
        return response_json, response.status_code
        
    def advanced_query(self, form_name, query, return_values=None, payload={}):
        """
        advanced_query is a member function used to gather form data
        based on a form name and request ID
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :type form_name: str
        :param req_id: the request ID of the desired entry
        :type req_id: str
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :type payload: dict, optional
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        if return_values is None:
            # Will return the complete form
            fields = ""
        else:
            field_list = ', '.join(return_values)
            fields = "fields=values({})&".format(field_list)
        
        url = self.base_url + REQUEST_PREFIX + "/{}?{}q={}".format(form_name, fields, query)

        response = requests.request("GET", url, headers=self.reqHeaders, verify=self.verify,
                                    proxies=self.proxies, timeout=self.timeout)
        response.raise_for_status()                                    

        return response.json(), response.status_code

    def attach_file_to_incident(self, req_id, filepath, filename, content_type='text/plain', details=None, view_access='Public', payload={}):
        """
        attach_file_to_incident is a member function used to update form data
        based on a form name and request ID
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :type form_name: str
        :param req_id: the request ID of the desired entry
        :type req_id: str
        :param values: dict of incident values to update
        :type values: dict
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :type payload: dict, optional
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        # Retrieve Entry ID from form to use on modify entry
        form_name="HPD:Help Desk"
        incident, status_code = self.advanced_query(form_name, "'Incident Number'=\"{}\"".format(req_id), ["Entry ID"])

        entry_id = incident['entries'][0]["values"]["Entry ID"]

        # Create attachment URL and values
       
        values = {
                "z1D_Details": "{}".format(details if details is not None else "No details entered"),
                "z1D_View_Access": "{}".format(view_access if view_access is not None else "Public"),
                "z1D_Activity_Type": "General Information",
                "z1D_Secure_Log": "Yes",
                "z2AF_Act_Attachment_1": "{}".format(filename)
                }

        # Create the files multipart submission

        # Cannot send files larger than 10MB (10*1024*1024)
        #   If larger, send the bottom 10MB (where incident issues will likely be)
        try:
            size = getsize(filepath+sep+filename)
            with open(f'{filepath+sep+filename}', 'rb') as file:
                # Do not read more than 10MB of the file 
                if size >= 10 * 1024 * 1024 :
                    # File is bigger than 10MB, so read the last 10MB
                    file.seek(-10 * 1024 * 1024, SEEK_END)  # Note minus sign
                # Read the remaining of the file (or all of it)
                content = file.read()
        except:
            content = 'File {} could not be read'.format(filepath+sep+filename)

        # Add json to the multipart submission
        files = {}
        # None in the first part will not show a filename.
        # need to use json.dumps with the encode. str(values) will not work.
        files['entry'] = (None, json.dumps({'values': values}).encode('utf-8'), 'application/json')
        files['attach-z2AF_Act_Attachment_1'] = (filename, content, content_type)

        url = self.base_url + REQUEST_PREFIX + "/{}/{}".format(form_name, entry_id)

        reqHeaders = {'Authorization': self.reqHeaders['Authorization']}
        response = requests.request("PUT", url, data=None, files=files, headers=reqHeaders, verify=self.verify,
                                     proxies=self.proxies, timeout=self.timeout)

        response.raise_for_status()
        
        # Remedy returns an empty 204 for form updates.
        # get the updated incident and return it with the update status code
        status_code = response.status_code
        updated_incident, _ = self.get_form_entry(form_name, entry_id, values)

        return updated_incident, status_code

    def add_worklog_to_incident(self, req_id, details, activity_type=None, view_access=None, secure_log=None, payload={}):
        """
        add_worklog_to_incident is a member function used to update form data
        based on a form name and request ID
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :type form_name: str
        :param req_id: the request ID of the desired entry
        :type req_id: str
        :param values: dict of incident values to update
        :type values: dict
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :type payload: dict, optional
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        # Retrieve Entry ID from form to use on modify entry
        form_name="HPD:Help Desk"
        incident, status_code = self.advanced_query(form_name, "'Incident Number'=\"{}\"".format(req_id), ["Entry ID"])

        entry_id = incident['entries'][0]["values"]["Entry ID"]

        # Create attachment URL and values
       
        values = { "values": 
            {
                "z1D_Details": "{}".format(details if details is not None else "No details entered"),
                "z1D_View_Access": "{}".format(view_access or "Public"),
                "z1D_Activity_Type": activity_type or "General Information",
                "z1D_Secure_Log": secure_log or "Yes"
            }
        }

        url = self.base_url + REQUEST_PREFIX + "/{}/{}".format(form_name, entry_id)

        response = requests.request("PUT", url, json=values, headers=self.reqHeaders, verify=self.verify,
                                     proxies=self.proxies, timeout=self.timeout)

        response.raise_for_status()
        
        # Remedy returns an empty 204 for form updates.
        # get the updated incident and return it with the update status code
        status_code = response.status_code
        updated_incident, _ = self.get_form_entry(form_name, entry_id, values)

        return updated_incident, status_code