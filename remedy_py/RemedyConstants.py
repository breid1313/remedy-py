# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Brian Reid, Ryan Gordon
# MIT License
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Changelog
###############################################################################
# When       # Who                    # What
###############################################################################
# 2023 01 08 # Daniel Companeetz      # Moved here constants from class module


# Constant values
DEFAULT_HTTP_PORT = 8008
DEFAULT_HTTPS_PORT = 8443

# Class constants
REQUEST_PREFIX = "/arsys/v1/entry"
DEFAULT_TIMEOUT = 30

# Interpreted values
HTTP_BASE_URL = lambda host, port: "http://{0}:{1}/api".format(host, str(port))
HTTPS_BASE_URL = lambda host, port: "https://{0}:{1}/api".format(host, str(port))