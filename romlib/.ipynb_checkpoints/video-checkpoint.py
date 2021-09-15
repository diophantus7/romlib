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
"""
Contains the classes needed to generate a video from the html of the source
page. The video class holds all useful information of a video.
"""
import sys
import urllib
import re

try: 
        from BeautifulSoup import BeautifulSoup
except ImportError:
        from bs4 import BeautifulSoup
        
from .wistia import WistiaExtractor
from .constants import RomwodConst
        
    
class Video(object):
    """Holds the necessary info of a romwod video.

    The class holds all the info that is useful for displaying information on a
    romwod video, like title, duration, et cetera. When referring to a video,
    we will mean a romwod video. It also stores/extracts the location of the
    video for different formats.

    Attributes:
        title: The title of the romwod video.
        duration: The duration of the video in seconds.
        description: A description of the video.
        tags: A list containing all the tagged poses.
        thumbnail: The link to the thumbnail of the video.
    """


    def __init__(self, video_block):
        """Initializes a video from a video_block.

        Args:
            video_block: A html code block containing information about the
                video.
        """
        self.title = video_block['title']
        self.duration = video_block['shortDurationInSeconds']
        self.description = video_block['description']
        self.tags = [tag['content'] for tag in video_block['poses']]
        self.link = RomwodConst.WORKOUTS_URL + video_block['slug']
        self.thumbnail = video_block['thumbnail']['url']
        wistia_id = video_block['shortExternalId']
        self._we = WistiaExtractor(wistia_id)
        self._urls = self._we.get_video_urls_and_formats()

    def duration_in_min(self):
        """Returns the duration of the video in minutes."""
        return int(divmod(self.duration, 60)[0])

    def get_an_url(self):
        """Returns the URL for the format 1080p."""
        return self.get_url_for_format('Original file')

    def get_url_for_format(self, format):
        """Returns a dict of format and url for that format or None if no
        format is available.

        Returns:
            An URL of the video location of the desired format. If no video is
            avaialble for the desired format, None is returned.
        """
        if format in self._urls:
            return self._urls[format]
        else:
            return None



class VideoBlocksHandler(object):
    """Handels the html code of all video blocks

    Splits the html code of all videos into blocks for each video and then
    creates a Video object for each block.
    """
    
    
    def __init__(self, video_blocks):
        """Instanciates the class.

        Args:
            video_blocks: html code of all videos on a given side.
        """
        self._video_blocks = video_blocks
        
    def get_videos(self):
        """
        Extracts each html video block and instanciates
        a Video for it. Returns all videos in a list.
        
        Returns:
            A list of Videos for each video block of html code.
        """
        videos = []
        for vid_blk in self._video_blocks:
            video = Video(vid_blk)
            videos.append(video)
        return videos

        
