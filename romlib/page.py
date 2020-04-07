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
"""Contains classes specific to handling the content of romwod pages"""

import requests
import re
import urllib.parse
import json
from collections import OrderedDict

try: 
        from BeautifulSoup import BeautifulSoup
except ImportError:
        from bs4 import BeautifulSoup
        
#from downloader import (DownloadHandler, LoginError)

from utils import get_daytime


class RomwodConst(object):
    HOST = "app.romwod.com"
    BASE_URL = "https://app.romwod.com/"
    WORKOUTS_URL = BASE_URL + "routine/"
    WOD_URL = BASE_URL + "wod?user_date="
    LOGIN_URL = BASE_URL + 'api/v2/auth/sign_in'


class RomwodPage(object):
    """Manages the content of a romwod page.

    This class manages the content of a romwod page. It can extract certain
    elements like video_blocks with information to construct Video objects.

    Attributes:
        content: The html content of the page.
    """
    
    def __init__(self, url, needs_login=False):
        """Construct the RomwodPage object.
        
        Args:
            url: The URL of the page to get information from.
            needs_login: Boolean indicating wheather a login is necessary to
                view the page.
        """
        self._url = url
        if needs_login:
            session = DownloadHandler()
        else:
            session = requests.session()
        self._content = session.get(url).content
        redirect = self._redirects()
        if redirect:
            self._content = session.get(redirect).content
        self._parser = BeautifulSoup(self._content)
        if self._is_login_page():
            raise LoginError("Page %s needs login." % self._url)
    
    def _redirects(self):
        """Checks if the url redirects."""
        soup = BeautifulSoup(self._content)
        location = re.search('window\.location\s*=\s*\"([^"]+)\"', str(soup))
        if location:
            return location.group(1)
        else:
            return False
        
    def _is_login_page(self):
        """Checks if the page is the login page."""
        if self._parser.findAll('div', {'id':'forgotPass'}):
            return True
        else:
            return False
  
    @property
    def content(self):
        return self._content

    def extract_video_blocks(self):
        """
        Extracts the video block from the html code as used on
        the romwod site.
        """
        parsed_html = BeautifulSoup(self._content)
        video_dict = self._parser.find('div', {'data-react-class':'WeeklySchedule'})
        if video_dict is not None:
            video_blocks = [video_block['video'] for video_block in json.loads(video_dict['data-react-props'])['schedule']['scheduled_workouts']]
        else:
            video_dict = self._parser.find('div', {'data-react-class':'SearchGrid'})
            video_blocks = json.loads(json.loads(video_dict['data-react-props'])['items'])
        return video_blocks
    
    def extract_selection_form(self):
        """
        Extracts the selection form which is used to filter the workouts
        by classes.
        """
        bs = BeautifulSoup(self._content)
        form = bs.body.find('form',
                            attrs={'class':'searchandfilter class_filter_search'})
        return str(form)    
    
    def extract_options(self):
        """Extracts the options for which one can filter the workouts."""
        form = BeautifulSoup(self.extract_selection_form(),
                             convertEntities=BeautifulSoup.HTML_ENTITIES)
        options = OrderedDict()
        for filterColumn in form.findAll('div', {'class':re.compile('filterColumn.*')}):
            options[filterColumn.h6.text]['options'] = OrderedDict()
            options[filterColumn.h6.text]['slug'] = filterColumn.find('a')['href'].split('?')[1].split('=')[0]
            for opt in filterColumn.findAll('a'):
                options[filterColumn.h6.text][opt['href'].split('=')[1]] = opt.text
                
        return options


    def next_page(self):
        """
        Checks for pagination.
        If this is the case, the next page is returned,
        otherwise None.
        """
        bs = BeautifulSoup(self._content)
        next = bs.find('a', attrs={'class':'next always-show'})
        if next:
            return next['href']
        else:
            return None
    

class Dashboard(RomwodPage):
    """The Dashboard is the main page of the romwod app.

    The Dashboard class contains entries not found on other romwod pages.
    """
    
    def __init__(self, url = RomwodConst.BASE_URL, needs_login = False):
        """Inits the class."""
        RomwodPage.__init__(self, url, needs_login)
        
    @property
    def dashboard_entries(self):
        """Returns a list of all dashboard entries."""
        return self._parser.findAll('div', {'class':'card_inner'})
    
    @property
    def dashboard_fanart(self):
        """Returns the fanart of the dashboard depending on the daytime."""
        fanart = FANART_BASE + 'dash-bg-' + get_daytime() + '.jpg'
        return fanart
    
    
