#!/usr/bin/env python
# general imports
import json
import requests
# import from our own API tools
from .utils import retry_on_server_error, retry_on_auth_and_error, retry_on_login_error

# suppresses invalid cert warnings, depricated..., using verify=False
requests.packages.urllib3.disable_warnings()

__author__ = 'JefityJefferson'


class pelotonAPIManager:
    """API session base class

    This class creates a connection object used to manage API sessions

        Attributes:
            self.base_url (str): server URL e.g. https://api.onepeloton.com/api
            self.logon_url (str): url used to make auth request
            self.logout_url (str): url used to close teardown our session
            self.user (str): API username, peloton email or username
            self.passwd (str): API password, peloton password

        Notes:

            @retry_on_server_error = decorator used to retry on any HTTP 500+ errors
            @retry_on_auth_and_error = decorator used to retry on any HTTP 400+ errors

    """

    def __init__(self, user, passwd):
        self.base_url = 'https://api.onepeloton.com'
        self.logon_url = '/auth/login'
        self.logout_url = '/auth/logout'
        self.user = user
        self.passwd = passwd
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent':'0.0.1'
        }

    def check_for_reauth(self, resp):
        if resp.text == 'Invalid Credential':
            self.login()
            print('Re-auth session for {}, done!'.format(self.user))

    @retry_on_login_error
    def login(self):
        """Creates login request to Peloton

        Pulls session token and updates headers on succesful login.
        all future request post/get/delete.

        """
        url = self.base_url + self.logon_url
        payload = {'username_or_email': self.user, 'password': self.passwd}
        try:
            resp = requests.post(url, headers=self.headers, data=json.dumps(payload), timeout=30, verify=False)
            if resp.ok:
                #self.headers.update(json.loads(resp.text))
                print('hit login print')
            else:
                print('Could not login to {url} -->{}'.format(resp.text))
            return resp

        except requests.exceptions.ConnectionError:
            print('Connection Timed out --> {}'.format(url))

    @retry_on_server_error
    def logout(self):
        url = self.base_url + self.logout_url
        resp = requests.post(
            url, headers=self.headers, timeout=30, verify=False)
        if not resp.ok:
            print("Failed to logout: {url}")
        return resp

    @retry_on_auth_and_error
    def put(self, url, data, timeout=1200):
        url = self.base_url + url
        resp = requests.put(
            url,
            headers=self.headers,
            data=data,
            timeout=timeout,
            verify=False)
        if not resp.ok:
            print('Error: {} --> {resp.text}'.format(url))
            self.check_for_reauth(resp)
        return resp

    @retry_on_auth_and_error
    def post(self, url, data, timeout=1200):
        url = self.base_url + url
        resp = requests.post(
            url,
            headers=self.headers,
            data=data,
            timeout=timeout,
            verify=False)
        if not resp.ok:
            print('Error: {} --> {resp.text}'.format(url))
            self.check_for_reauth(resp)
        return resp

    @retry_on_auth_and_error
    def get(self, url):
        url = self.base_url + url
        resp = requests.get(
            url, headers=self.headers, timeout=30, verify=False)
        if not resp.ok:
            print('Error: {} --> {resp.text}'.format(url))
            self.check_for_reauth(resp)
        return resp

    @retry_on_server_error
    def delete(self, url):
        url = self.base_url + url
        resp = requests.delete(url, headers=self.headers, verify=False)
        if not resp.ok:
            print('Error: {} --> {resp.text}'.format(url))
            self.check_for_reauth(resp)
        return resp

