# Overview
`remedy-py` is a Python package used to interface with the BMC Remedy REST API.
My search for a development tool to facilitate easy interactions with the Remedy API
in a Python program didn't turn up any results that suited my needs, so I decided to create
my own and open-source it. Your feedback and contributions are welcome (see [Contributing](#Contributing)), so
that we can make this package useful to as many people as possible.

## Installation
You may install `remedy-py` directly from [PyPI](https://pypi.org/project/remedy-py/), or via pip:
`pip install remedy-py`. 

## Usage

### Import the Package
Once you have the package installed, import the RemedyClient class for use in your Python program as follows:
`from remedy_py.RemedyAPIClient import RemedyClient`

### Instantiate a Client
The `RemedyClient` constructor has three required arguments: `host`, `user`, and `password`.
Optional positional arguments include `verify`, `proxies`, and `timeout`.
Once you have instantiated a client, authentication with the Remedy API
is automatically handled for you in the constructor based on the username 
and password provided. Any subsequent calls to the API will include a user-specific
jwt in the headers to let Remedy know who you are.

Example usage:
`client = RemedyClient("example.domain", "Allen", "password", verify=False)`

### Create a form entry

``` python
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

FORM_NAME = "HPD:IncidentInterface_Create"
RETURN_VALUES = ["Incident Number", "Request ID"]

incident, status_code = client.create_form_entry(FORM_NAME, ENTRY_TEMPLATE, RETURN_VALUES)
incident_id = incident["values"]["Incident Number"]
request_id = incident["values"]["Request ID"]
```

## New in the latest release

### Run an advanced query

advanced_query is a member function used to gather form data based on a form name and a query provided by the user.

The function returns: a tuple with the response content as json and the http status code.

Provide the following parameters:

- form_name: name of the form to query
- query: properly formatted query (no validation by the function). You may want to implement code injection verification protocols.
- return_values: list of value/keys to return from the form (returns the complete form if None (default))

### Add a worklog to an incident

add_worklog_to_incident is a member function used to add a worklog entry to the incident based on the incident ID the user knows. (uses advanced query to get the Entry ID requried from the HPD:Help Desk form.)

The function returns: a tuple with the updated Incident content as json and the http status code.

Provide the following parameters:

- req_id: Incident ID to which the worklog will be added
- details: Text that will appear in the Notes
- activity_type: (optional) Activity type: Defaults to General Information if None
- view_access:  (optional) Public if None
- secure_log: (optional) Yes if None

``` python
req_id = incident_id
details = f"This updated via REST API for incident {incident_id}"

updated_incident, status_code = client.add_worklog_to_incident(req_id, details)

```

### Attach a file to an incident

attach_file_to_incident is a member function used to attach a file to an incident

The function returns: a tuple with the updated incident as json (dict), and the http status code (should be 204, as the content is empty). This method may be made general for any form, but since it could not be tested,  "HPD:Help Desk" was set as a default form.

- req_id: Incident ID to which the file will be added
- filepath: File path to the attachment
- filename: File name of the attachment
- form_name: (optional) form to attach the file to. ('HPD:Help Desk' default)
- view_access:  (optional) Public if None
- secure_log: (optional) Yes if None

``` python
req_id = incident_id
tmpdir = tempfile.gettempdir()
file_log = f"log_{runId}_{runNo}.txt"

updated_incident, status_code = client.attach_file_to_incident(req_id=incident_id, 
    filepath=tmpdir, filename=file_log, details="Helix Control-M Log file")
```

## Contributing

Your feedback and contributions are welcome through issues and pull requests on the GitHub repository.
Please be as descriptive as possible with issues or feature requests and provide testing instructions
with any pull requests.

Thank you for helping to advance this project!

### Contributors

Special shout out to my good friend and colleague Ryan Gordon (@Ryan-Gordon & @Ryan-Gordon1)
for helping get this off the ground. I appreciate your open and honest feedback and bright ideas.

Additional Contributors

| Date | Who | What |
| - | - | - |
| 2023-01-19 | Daniel Companeetz | advanced_query, add_worklog_to_incident, attach_file_to_incident |
