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

#_IFRAME_URL = "https://embedwistia-a.akamaihd.net/deliveries/%s"


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
    
    
    def get_video_url(self, format):
        """gets the video url

        Retrieves the url of the wistia video with the video id self.video_id
        with the specified format.

        Args:
            format: A possible format of the video.

        Returns:
            The URL of the video with the given format. If that video does not
            exist return any format

        Raises:
            ResolveError: No format found in the json data
        """
        json_data = self._download_json()
        # 17.4.2018 json_data['media']['assets'][0]['url'] is the standard today
        #return json_data['media']['assets'][0]['url']
        try:
            url = next(d['url'] for d in self._json_data['media']['assets']
                    if d['display_name'] == format and d['ext'] == 'mp4')
        except:
            video_data = [d for d in self._json_data['media']['assets']
                         if d['status'] == 2 and 'opt_vbitrate' in d
                         and 'display_name' in d and
                         'p' in d['display_name']]
            if not video_data:
                raise ResolveError("No video found.")
            url = max(video_data,
                      key=lambda d: int(d['display_name'].strip('p')))['url']
        return url


