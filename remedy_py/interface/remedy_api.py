# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Brian Reid, Ryan Gordon
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import abc

# There is a difference between have abstract base classes are handled in py 2 and 3
# In python 3 we can directly access abc.ABC and inherit from that
# In python 2 we must create the ABC class using abc.ABCMeta
if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta


class RemedyAPI(ABC):
    @abc.abstractmethod
    def get_token(self, *args, **kwargs):
        raise NotImplementedError(
            "Child classes must implement all methods of the RemedyAPI interface."
        )

    @abc.abstractmethod
    def build_request_headers(self, *args, **kwargs):
        raise NotImplementedError(
            "Child classes must implement all methods of the RemedyAPI interface."
        )

    @abc.abstractmethod
    def release_token(self, *args, **kwargs):
        raise NotImplementedError(
            "Child classes must implement all methods of the RemedyAPI interface."
        )

    @abc.abstractmethod
    def create_form_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "Child classes must implement all methods of the RemedyAPI interface."
        )

    @abc.abstractmethod
    def get_form_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "Child classes must implement all methods of the RemedyAPI interface."
        )

    @abc.abstractmethod
    def update_form_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "Child classes must implement all methods of the RemedyAPI interface."
        )

    @abc.abstractmethod
    def delete_form_entry(self, *args, **kwargs):
        raise NotImplementedError(
            "Child classes must implement all methods of the RemedyAPI interface."
        )
