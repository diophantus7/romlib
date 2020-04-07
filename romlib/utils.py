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
import re
import datetime
from collections import OrderedDict

try: 
        from BeautifulSoup import BeautifulSoup
except ImportError:
        from bs4 import BeautifulSoup


def extract_selection_form(site):
    """
    Extracts the selection form which is used to filter the workouts
    by classes
    
    :param site: str
    """
    bs = BeautifulSoup(site)
    form = bs.body.find('form',
                        attrs={'class':'searchandfilter class_filter_search'})
    return str(form)
    
def extract_options(site):
    """
    Extracts the options for which one can filter the workouts
    
    :param site: str
    """
    form = BeautifulSoup(extract_selection_form(site),
                         convertEntities=BeautifulSoup.HTML_ENTITIES)
    node = form.div.ul.li
    opt_dict = OrderedDict()
    while node.h4 is not None:
        opt_dict[node.h4.text] = [(x.text, x.input['name'][2:-2])
                                  for x in node.findAll('li')]
        node = node.nextSibling
    return opt_dict

    
def get_daytime():
    now = datetime.datetime.now()
    midnight = now.replace(hour=00, minute=0, second=0, microsecond=0)
    noon = now.replace(hour=12, minute=0, second=0, microsecond=0)
    time5pm = now.replace(hour=17, minute=0, second=0, microsecond=0)
    if midnight <= now < noon:
        return 'morning'
    elif noon <= now < time5pm:
        return 'afternoon'
    elif time5pm <= now:
        return 'evening'
    
    
