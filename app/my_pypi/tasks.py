import sys, os
from pathlib import Path
from typing import List, Optional
import re
import requests
import xml.etree.ElementTree as ET
import pathlib

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..")))

from my_pypi.bin import load_data 
'''
1)Schedule a task within some interval
2)get the data from the RSS - https://pypi.org/rss/packages.xml
3)check if the data is new (maybe to hash some text and compare it with the previes request(some caching))
4)collect the new urls
5)filter the packages - check that they are not already exists 
6)make a get request on each of them with https://warehouse.readthedocs.io/api-reference/json/
7)save the JSONs on the data folder
8)enter them to DB (????)
'''

PYPI_URL_NEWEST_PACKAGES='https://pypi.org/rss/packages.xml'
PYPI_URL_JSON_PACKAGE='https://pypi.org/pypi/PACKAGE/json'

def get_newest_packages_from_pypi() -> Optional[str]: 
    ''' Using the RSS URL'''
    data = requests.get(PYPI_URL_NEWEST_PACKAGES)
    if data.status_code != 200:
        return None
    return data.text
    
#4)collect the new urls
def collect_urls(data_xml : str) -> List:
    ''' Parse the XML and return the urls(entire format)'''
    xmliter = ET.fromstring(data_xml).iter()
    urls = []
    for element in xmliter:
        if element.tag == 'link':
            l = element.text
            urls.append(l)
    return urls

#5)check that they are not already exists
def is_package_exists(package : str) -> str:
    '''Check if package exists'''
    curr_path = Path(__file__).parent.absolute()
    p = Path(str(curr_path) + r"/../data/pypi-packages/" + package + '.json')
    return p.exists()

#6)make a get request on each of them with https://warehouse.readthedocs.io/api-reference/json/
def save_new_package(package_name : str):
    '''Fetch the package json from pypi and save it as a file '''
    url = PYPI_URL_JSON_PACKAGE.replace('PACKAGE', package_name)
    #download json TODO:Async request? multi-threaded?
    print("downloading... " + url)
    req = requests.get(url)
    if req.status_code == 200:
        print("ok")
        curr_path = Path(__file__).parent.absolute()
        p = Path(str(curr_path) + r"/../data/pypi-packages/")#TODO:save it on DB
        fn = package_name + '.json'
        filepath = p / fn
        with filepath.open("x+", encoding ="utf-8") as f:
            f.write(req.text)

def get_package_name_from_url(url : str) -> Optional[str]:
    '''find the package name from url
        Example: url -> 'https://pypi.org/project/perceptilabs/' will return -> 'perceptilabs' '''
    package_name = re.findall(r'\/(?:[a-z0-9]+[_-]*)*[a-z0-9]\/$', url)
    if len(package_name) != 1:
        return None
    return package_name[0].replace('/', '')

def task():
    packages_added = 0
    data = get_newest_packages_from_pypi()
    urls = collect_urls(data)
    for url in urls:
        package_name = get_package_name_from_url(url)
        if package_name:
            if not is_package_exists(package_name):
                packages_added += 1
                save_new_package(package_name)
                print(package_name)
    print(str(packages_added) + " new packages added!")
    return packages_added

def main():
    new_packages = task()
    if new_packages:
        load_data.load()

if __name__ == '__main__':
    main()

