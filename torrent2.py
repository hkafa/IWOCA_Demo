from bs4 import BeautifulSoup
import requests

def find_torrent_list(search_string):
    list_of_titles = {'titles':[],  'magnets':[], 'size':[], 'timestamp':[]}

    source = requests.get('https://thepiratebay.zone/search/{}'.format(search_string)).text
    soup = BeautifulSoup(source, 'lxml')

    for i in soup.find_all('a', class_='detLink'):
        if 'Details for' in i['title']:
            title_string = i['title'].split('Details for')
            list_of_titles['titles'].append(title_string[1])

    for link in soup.find_all('a'):
        i = link.get('href')
        if 'magnet' in i:
            list_of_titles['magnets'].append(i)

    for size in soup.find_all('font', class_='detDesc'):
        size = str(size).split(',')[1].split('Size')[1]
        size = size.replace(u'\xa0', u' ')
        list_of_titles['size'].append(size)

    for timestamp in soup.find_all('font', class_='detDesc'):
        timestamp = str(timestamp).split(',')[0].split('>')[1]
        timestamp = timestamp.replace(u'\xa0', u' ')
        list_of_titles['timestamp'].append(timestamp)

    return list_of_titles

def find_rating(search_string):
    try:
        source = requests.get(f'https://www.rottentomatoes.com/m/{search_string}').text
        soup = BeautifulSoup(source, 'lxml')
        meter = soup.find('span', class_='mop-ratings-wrap__percentage').text
        meter = meter.split('\n')[1].split()
        meter = (meter[0])
        return meter
    except AttributeError:
        meter = ' '
        return meter




