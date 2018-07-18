from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup


def get_soup(spell_name):
    spell_url = spell_name.replace(' ', '_')
    spell_url = quote(spell_url)
    page_path = 'http://engl393-dnd5th.wikia.com/wiki/' + spell_url
    page = urlopen(page_path)
    return BeautifulSoup(page, 'html.parser')


def get_info(soup):
    info_box = soup.find('div', attrs={'class': 'WikiaArticle'})
    table = info_box.find('table')
    info_items = table.find_all('tr')
    info_dict = dict()
    for item in info_items:
        key = item.find('th').text.strip()
        value = item.find('td').text.strip()
        info_dict[key] = value
    return info_dict


def get_level_and_type(soup):
    info_box = soup.find('div', attrs={'class': 'WikiaArticle'})
    table = info_box.find('table')
    caption = table.find('caption')
    return caption.text.strip().split()


def get_description(soup):
    info_box = soup.find('div', attrs={'class': 'WikiaArticle'})
    descriptions = info_box.find_all('p')
    spell_description = ''
    for description in descriptions:
        spell_description += description.text
    return spell_description
