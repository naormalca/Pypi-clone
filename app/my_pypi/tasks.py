from pathlib import Path
import re
import requests
import xml.etree.ElementTree as ET
import pathlib


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

#2)get the data from the RSS - https://pypi.org/rss/packages.xml
def get_newest_packages_from_pypi():
    data = requests.get(PYPI_URL_NEWEST_PACKAGES)
    if data.status_code != 200:
        return
    return data.text
    
#4)collect the new urls
def collect_urls(data_xml):
    xmliter = ET.fromstring(data_xml).iter()
    urls = []
    for element in xmliter:
        if element.tag == 'link':
            l = element.text
            urls.append(l)
    return urls

#5)filter the packages - check that they are not already exists
def filter_packages():
    pass

#6)make a get request on each of them with https://warehouse.readthedocs.io/api-reference/json/
#7)save the JSONs on the data folder
def save_new_package(url : str):
    #get the package name
    package_name = get_package_name_from_url(url)
    if package_name is not None:
        url = PYPI_URL_JSON_PACKAGE.replace('PACKAGE', package_name)
        #download json TODO:Async request? multi-threaded?
        print("downloading... " + url)
        req = requests.get(url)
        if req.status_code == 200:
            p = Path(r"../tmp/")
            p.mkdir(parents=True, exist_ok=True)
            fn = package_name + '.json'
            filepath = p / fn
            with filepath.open("w+", encoding ="utf-8") as f:
                f.write(req.text)

def get_package_name_from_url(url : str):
    package_name = re.findall(r'\/(?:[a-z0-9]+[_-]*)*[a-z0-9]\/$', url)
    if len(package_name) != 1:
        return None
    return package_name[0].replace('/', '')




data = get_newest_packages_from_pypi()
urls = collect_urls(data)
for l in urls:
    save_new_package(l)
