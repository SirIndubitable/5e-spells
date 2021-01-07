from urllib.request import urlopen
from urllib.parse import quote
import logging
import re
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

_format0 = re.compile("""(?P<level_and_type>.+)
Casting Time: (?P<cast_time>.+)
Range: (?P<range>.+)
Components: (?P<components>.+)
Duration: (?P<duration>.+?)
(?P<descr_n>.+)
""", re.MULTILINE | re.DOTALL )

def get_soup(spell_name):
    spell_url = spell_name.replace(' ', '_')
    spell_url = quote(spell_url)
    page_path = 'http://engl393-dnd5th.wikia.com/wiki/' + spell_url
    log.debug('parsing page: ' + page_path)
    page = urlopen(page_path)
    return BeautifulSoup(page, 'html.parser')


def parse_info(soup):
    info_box = soup.find('div', attrs={'class': 'mw-parser-output'})
    if info_box is None:
        return None
    match = _format0.match(info_box.text)
    if match is None:
        return None
    return { k:v.strip() for k, v in match.groupdict().items() }

