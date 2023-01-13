# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Brian Reid
# MIT License
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from remedy_py.RemedyAPIClient import RemedyClient
from mock import patch
import unittest

# Changelog
###############################################################################
# When       # Who                    # What
###############################################################################
# 2023 01 08 # Daniel Companeetz      # Adding unit testing for new INC methods


####
# Pass an obj argument to all the mocked methods
# python is implicitly passing self to each method call
# since we are testing in the context of a class
####

def mock_build_request_headers(obj):
    token = "foo"
    return {
            "content-type": "application/json",
            "Authorization": "AR-JWT " + token
        }

def mock_create_form_entry(obj, form_name, values, return_values=[]):
    mock_response = {
        "values": {
            'Incident Number': 'INC000000000301',
            'Request ID': '000000000000179'
        },
        "_links": {
            "self":
            [{
                "href": "foo"
            }]
        }
    }
    return mock_response, 201

def mock_get_form_entry(obj, form_name, req_id):
    mock_response = {
        "values": {
            'Incident Number': 'INC000000000301',
            'Request ID': '000000000000179'
        },
        "_links": {
            "self":
            [{
                "href": "foo"
            }]
        }
    }
    return mock_response, 200

def mock_update_form_entry(obj, form_name, req_id, values):
    return {}, 204

def mock_delete_form_entry(obj, form_name, req_id):
    return {}, 204

def mock_advanced_query(obj, form_name, query, return_values):
    response = {"entries":[
        {"values":
            {"Entry ID":"INC000000000001"},
            "_links":
                {"self":[
                    {"href":"foo"}
                    ]
                }
            }
        ],
        "_links":
            {"self":
                [
                    {"href":"foo"}
                    ]
                }
            }
    mock_response =   response  
    return mock_response, 200



class TestRemedyClient(unittest.TestCase):

    @patch('remedy_py.RemedyAPIClient.RemedyClient.build_request_headers', mock_build_request_headers)
    def setUp(self):
        self.form_name = "HPD:IncidentInterface_Create"
        self.client = RemedyClient("example.com", "foo", "bar")

    @patch('remedy_py.RemedyAPIClient.RemedyClient.create_form_entry', mock_create_form_entry)
    def test_create_form_entry(self):
        ENTRY_TEMPLATE = {
            "First_Name": "Allen",
            "Last_Name": "Allbrook",
            "Description": "REST API: Incident Creation",
            "Impact": "1-Extensive/Widespread",
            "Urgency": "1-Critical",
            "Status": "Assigned",
            "Reported Source": "Direct Input",
            "Service_Type": "User Service Restoration",
            "z1D_Action": "CREATE"
        }
        RETURN_VALUES = ["Incident Number", "Request ID"]

        response, status_code = self.client.create_form_entry(self.form_name, ENTRY_TEMPLATE)
        assert(status_code == 201)
        assert(response["values"])

    @patch('remedy_py.RemedyAPIClient.RemedyClient.get_form_entry', mock_get_form_entry)
    def test_get_form_entry(self):
        req_id = "INC0000000001"
        response, status_code = self.client.get_form_entry(self.form_name, req_id)
        assert(status_code == 200)
        assert(response["values"])

    @patch('remedy_py.RemedyAPIClient.RemedyClient.update_form_entry', mock_update_form_entry)
    def test_update_form_entry(self):
        req_id = "INC0000000001"
        entry = {
            "values": {
                "First Name": "Allen",
                "Last Name": "Allbrook"
            }
        }

        response, status_code = self.client.update_form_entry(self.form_name, req_id, entry)
        assert(status_code == 204)

    @patch('remedy_py.RemedyAPIClient.RemedyClient.delete_form_entry', mock_delete_form_entry)
    def test_delete_form_entry(self):
        req_id = "INC0000000001"
        response, status_code = self.client.delete_form_entry(self.form_name, req_id)
        assert(status_code == 204)

    
    @patch('remedy_py.RemedyAPIClient.RemedyClient.advanced_query', mock_advanced_query)
    def test_advanced_query(self, *args, **kwargs):
        req_id = "INC0000000001"
        form_name = 'HPD:Help Desk'
        response, status_code = self.client.advanced_query(form_name, "'Incident Number'=\"{}\"".format(req_id), ["Entry ID"])
        assert(status_code == 200)
        

    @patch('remedy_py.RemedyAPIClient.RemedyClient.attach_file_to_incident', mock_attach_file_to_incident)
    def attach_file_to_incident(self, *args, **kwargs):
        assert(status_code == 204)

    @abc.abstractmethod
    def add_worklog_to_incident(self, *args, **kwargs):
        assert(status_code == 200)
        

if __name__ == '__main__': 
    unittest.main()