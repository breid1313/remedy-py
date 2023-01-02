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
```python
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

## Contributing
Your feedback and contributions are welcome through issues and pull requests on the GitHub repository.
Please be as descriptive as possible with issues or feature requests and provide testing instructions
with any pull requests.

Thank you for helping to advance this project!

### Contributors
Special shout out to my good friend and colleague Ryan Gordon (@Ryan-Gordon & @Ryan-Gordon1)
for helping get this off the ground. I appreciate your open and honest feedback and bright ideas.
