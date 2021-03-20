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
"""Classes specific to wistia.

class Wistia contains constants specific to wistia.
class WistiaExtractor extracts the location of the video for a given resolution.

    Typical usage example:

    we = WistiaExtractor(12345, '720p')
    we.video_url()
"""
import re
import requests
import json

try: 
        from BeautifulSoup import BeautifulSoup
except ImportError:
        from bs4 import BeautifulSoup



class ResolveError(Exception):
    def __init__(self, message):
        self.message = message


class Wistia(object):
    JSON_URL = "http://fast.wistia.com/embed/medias/%s.json"
    IFRAME_URL = "http://fast.wistia.net/embed/iframe/%s"
        

class WistiaExtractor(object):
    """Handles the Wistia data and extracts videos.

    Given a wistia video id, it downloads all the avaialable json data of the
    video. It can retrive the url for the video for different formats.

    Attributes:
        video_id: The wistia video id of the video.
    """
    
    def __init__(self, video_id):
        self.video_id = video_id
        self._json_data = self._download_json()
    
        
    def _download_json(self):
        """Returns the json data of the video after downloading it."""
        s = requests.Session()
        s.headers.update({'referer':Wistia.IFRAME_URL % self.video_id})
        req = s.get(Wistia.JSON_URL % self.video_id)
        return req.json()
    
    
    def get_video_urls_and_formats(self):
        """gets the video URLs and formats

        Retrieves the URL of the wistia videos with the video id self.video_id
        for all formats.

        Returns:
            The URLs of the video for all formats. If json data is not of the
            regular format or no formats were found, then return None
        """
        # 17.4.2018 json_data['media']['assets'][0]['url'] is the standard today
        #return json_data['media']['assets'][0]['url']
        urls = {}
        if 'media' in self._json_data:
            for d in self._json_data['media']['assets']:
                res = d['display_name']
                if res.endswith('p') or res == 'Original file':
                    urls[res] = d['url']
        return urls

