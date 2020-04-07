# Copyright 2020 diophantus7
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Class handling the login to the romwod page."""

import sys
import os
import re
import requests
import pickle
import json

try: 
        from BeautifulSoup import BeautifulSoup
except ImportError:
        from bs4 import BeautifulSoup
        
from page import RomwodConst


class LoginError(Exception):
    def __init__(self, message):
        self.message = message


class LoginHandler(requests.Session):
    """Handles the sign in to the romwod page.

    Class takes the login credentials and logs into the romwod page or uses the
    cookies for the session. The class inherits from requests.Sessiosn to
    get content from the romwod page.

    Args:
        username: The username or email used to sign into the romwod page.
        password: The password used to sign in.
        cookie_path: The location of the cookie

    Raises:
        LoginError: An error occurred during the sign in.
    """
    
    def __init__(self, username, password, cookie_file=""):
        """Inits the class with the necessary data"""
        self._username = username
        self._password = password
        self._cookie_file = cookie_file
        super().__init__()
        
        if os.path.isfile(self._cookie_file):
            self.cookies = self._get_cookies()
        
        if (bool(self.cookies) is False or
            any(cookie.is_expired() for cookie in self.cookies
                 if cookie.name == '_romwod_session')):
            try:
                self._sign_in()
            except LoginError as err:
                raise LoginError(err.message)
            self._save_cookies()
    
    
    def _sign_in(self):
        """Posts the login data for the romwod page.
        
        Raises:
            LoginError: Error if the username/password combo is wrong or if no
            username and password are given."""
        if self._username and self._password:
            login_data = dict(email = self._username, password = self._password)
            r = self.post(RomwodConst.LOGIN_URL, data=login_data)
            d = json.loads(r.content.decode())
            if 'errors' in d: 
                raise LoginError(d['errors'][0])
        else:
            raise LoginError("Please specify username and password.")



    def _save_cookies(self):
        """Saves the cookies from the login to the file given."""
        with open(self._cookie_file, 'wb') as f:
            pickle.dump(self.cookies, f)
        
        
    def _get_cookies(self):
        """Loads the cookies for the romwod session."""
        with open(self._cookie_file, 'rb') as f:
            return pickle.load(f)
        
        
