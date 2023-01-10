# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Brian Reid
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# pragma pylint: disable=unused-argument, no-self-use, undefined-variable

from typing import Any, List, Optional, Tuple

import requests

from .interface.remedy_api import RemedyAPI
# Load constant values for API Calls
from .RemedyConstants import *

REQUEST_PREFIX = "/arsys/v1/entry"
DEFAULT_TIMEOUT = 30


class RemedyClient(RemedyAPI):
    def __init__(
        self,
        host,
        username,
        password,
        port=None,
        verify=True,
        proxies=None,
        timeout=DEFAULT_TIMEOUT,
    ):
        self.host = host
        self.username = username
        self.password = password
        self.verify = verify
        self.proxies = proxies if proxies else {}
        self.timeout = timeout
        self.port = (
            port or DEFAULT_HTTPS_PORT if self.verify else port or DEFAULT_HTTP_PORT
        )
        self.base_url = (
            HTTPS_BASE_URL(self.host, self.port)
            if self.verify
            else HTTP_BASE_URL(self.host, self.port)
        )
        self.authHeaders = {"content-type": "application/x-www-form-urlencoded"}
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

        response = requests.request(
            "POST",
            url,
            data=data,
            headers=self.authHeaders,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        response.raise_for_status()
        token = response.content
        encoding = response.apparent_encoding
        token = token.decode(encoding)

        return token

    def build_request_headers(self):
        """
        Builds the request headers that Remedy expects
        for calls to the REST API

        :return: dict of request headers
        :rtype: dict
        """
        token = self.get_token()
        req_headers = {
            "content-type": "application/json",
            "Authorization": "AR-JWT " + token,
        }

        return req_headers

    def release_token(self):
        """
        Releases a JWT token so that it cannot be used
        for further interaction with the REST API.
        The function returns: a tuple with the response content as json and the http status code.

        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        url = self.base_url + "/jwt/logout"

        response = requests.request(
            "POST",
            url,
            headers=self.reqHeaders,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        response.raise_for_status()

        # logging off returns an empty 204
        # return empty json in the absence of response/incident content
        response_json = response.json() if response.content else {}

        return response_json, response.status_code

    def create_form_entry(
        self,
        form_name: str,
        values: dict,
        return_values: Optional[List[str]] = None,
        payload: Optional[dict] = None,
    ) -> Tuple[Any, int]:
        """
        create_form_entry is a member function used to take a payload
        and form name and use it to create a new entry on the Remedy system.
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to add an entry for
        :param values: dictionary of incident values
        :param return_values: list of field names to return from the created entry
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        if not return_values:
            return_values = []
        if not payload:
            payload = {}

        field_list = ", ".join(return_values)
        url = (
            self.base_url
            + REQUEST_PREFIX
            + "/{}?fields=values({})".format(form_name, field_list)
        )
        entry = {"values": values}

        response = requests.request(
            "POST",
            url,
            json=entry,
            headers=self.reqHeaders,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        response.raise_for_status()

        return response.json(), response.status_code

    def get_form_entry(
        self, form_name: str, req_id: str, payload: Optional[dict] = None
    ) -> Tuple[Any, int]:
        """
        get_form_entry is a member function used to gather form data
        based on a form name and request ID
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :param req_id: the request ID of the desired entry
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        if not payload:
            payload = {}

        url = self.base_url + REQUEST_PREFIX + "/{}/{}".format(form_name, req_id)
        response = requests.request(
            "GET",
            url,
            headers=self.reqHeaders,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        response.raise_for_status()

        return response.json(), response.status_code

    def update_form_entry(
        self, form_name: str, req_id: str, values: dict, payload: Optional[dict] = None
    ) -> Tuple[Any, int]:
        """
        update_form_entry is a member function used to update form data
        based on a form name and request ID
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :param req_id: the request ID of the desired entry
        :param values: dict of incident values to update
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        if not payload:
            payload = {}

        entry = {"values": values}
        url = self.base_url + REQUEST_PREFIX + "/{}/{}".format(form_name, req_id)

        response = requests.request(
            "PUT",
            url,
            json=entry,
            headers=self.reqHeaders,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        response.raise_for_status()

        # Remedy returns an empty 204 for form updates.
        # get the updated incident and return it with the update status code
        status_code = response.status_code
        updated_incident, _ = self.get_form_entry(form_name, req_id, values)

        return updated_incident, status_code

    def delete_form_entry(
        self, form_name: str, req_id: str, payload: Optional[dict] = None
    ) -> Tuple[Any, int]:
        """
        delete_form_entry is a member function used to delete
        a form entry based on a form name and request ID.
        The function returns: a tuple with the response content as json and the http status code.

        :param form_name: name of the form to query
        :param req_id: the request ID of the desired entry
        :param payload: Any extra options you want to include on the incident, defaults to {}
        :return: the response content and http status code as a tuple
        :rtype: tuple(json, int)
        """
        if not payload:
            payload = {}

        url = self.base_url + REQUEST_PREFIX + "/{}/{}".format(form_name, req_id)
        response = requests.request(
            "DELETE",
            url,
            headers=self.reqHeaders,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        response.raise_for_status()

        response_json = response.json() if response.content else {}

        # Remedy returns an empty 204 for form deletion.
        # return empty json in the absence of response/incident content
        return response_json, response.status_code
