"""
Requests + responses objects for API testing
"""
import json
import sys
from pprint import pprint

import allure
from jsonmodels.models import Base
from requests import ReadTimeout, Session, Request, RequestException

from .logging_utils import autolog, LOG_LEVEL

DEFAULT_HEADER = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


class ApiRequest(Request):
    """Base class for all requests to backend API"""

    def __init__(self, url, service_url=None, method='POST', **kwargs):
        """
        :param url: url of handler. As listed in docs (without host). Mandatory.
        :type url: str
        :param method: HTTP method to use, mandatory in parent class
        :type method: str
        :param service_url: FQDN of the service we requesting
        :type service_url: str
        """
        self.base_url = service_url
        self.url = self.base_url + url  # To get the real handler

        if 'headers' not in kwargs.keys():
            headers = DEFAULT_HEADER
        else:
            headers = kwargs['headers']
            del kwargs['headers']

        if 'name' in kwargs.keys():  # necessary for logging during load testing
            autolog(kwargs['name'])
            del kwargs['name']
        else:
            autolog(self.url)

        # Fail-safe in case we received instance of jsonmodels.models.Base (aka object of JSON)
        if 'json' in kwargs.keys():
            if isinstance(kwargs['json'], Base):
                kwargs['json'] = kwargs['json'].to_struct()
                autolog('Implicitly converted JSON object to dict!', 'debug')

        super(ApiRequest, self).__init__(url=self.url, method=method, headers=headers, **kwargs)

        self.prepared_request = self.prepare()
        self.session = Session()
        self.response = None

    @allure.step('Requesting API')
    def perform(self, check_ok=True, timeout=10, **kwargs):
        """Prepare and perform request to backend API

        :param check_ok: check if request went successful
        :param timeout: http timeout for the request
        :param verify: for verifying SSL certificate
        :return response: `Response` instance
        """
        log_level = LOG_LEVEL
        if 'log_level' in kwargs.keys():
            log_level = kwargs['log_level']
            del kwargs['log_level']

        autolog(f'Requesting: {self.method} {self.prepared_request.url}')
        allure.attach(repr(self.prepared_request.headers), name=f'{self.method} {self.url} request headers',
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(repr(self.prepared_request.body), name=f'{self.method} {self.url} request body',
                      attachment_type=allure.attachment_type.JSON)
        if self.params:
            allure.attach(repr(self.params), name=f'{self.method} {self.url} request params',
                          attachment_type=allure.attachment_type.TEXT)
        try:
            self.response = self.session.send(self.prepared_request, timeout=timeout, **kwargs)
        except ReadTimeout as e:
            autolog(f'Failed to get answer for {e.request.method} to {e.request.path_url}', 'error')
            autolog(f'Request header:\n {e.request.headers} \n', 'error')
            autolog(f'Request body: \n {e.request.body} \n', 'error')
            raise e

        autolog(f'Got response: {self.response.status_code}')

        autolog(f'REQUEST HEADERS: {self.response.request.headers}')
        autolog(f'REQUEST BODY: {self.response.request.body}', log_level)
        autolog(f'RESPONSE TIME: {self.response.elapsed.total_seconds() * 1000:.0f} ms')
        autolog(f'RESPONSE HEADERS: {self.response.headers}', log_level)
        autolog(f'RESPONSE BODY: {self.response.text}', log_level)

        allure.attach(repr(self.response.headers), name=f'{self.method} {self.url} raw response headers',
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(repr(self.response.text), name=f'{self.method} {self.url} raw response text',
                      attachment_type=allure.attachment_type.JSON)

        if len(self.response.content) > 0:
            try:
                # We almost every time need this JSON from data:
                self.response.decoded_body = self.response.json()
            except Exception as e:
                autolog("Can't decode JSON body", 'warning')
                autolog(e, 'warning')

        if check_ok:
            try:
                assert self.response.ok
            except AssertionError:
                # Throw custom exception
                raise ApiException(self.response, self.prepared_request) from AssertionError

        return self.response


class ApiException(RequestException):
    """Wrapper for exception in API call"""

    def __init__(self, response, prepared_request, *args, **kwargs):
        autolog(f'Request went bad: {response.status_code} {response.reason}', 'error')
        autolog('Prepared request: \nHeader:')
        pprint(prepared_request.headers, stream=sys.stderr)
        if prepared_request.body:
            autolog('Body:', 'error')
            autolog(json.dumps(json.loads(prepared_request.body), indent=2), 'error')
        autolog('Response:')
        pprint(response.headers, stream=sys.stderr)
        pprint(response.text, stream=sys.stderr)
        # Save request and response data for further checks
        self.api_response = response
        self.api_prepared_request = prepared_request
        self.api_response.decoded_body = self.api_response.json()
        super(ApiException, self).__init__(*args, **kwargs)
