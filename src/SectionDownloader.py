import logging
import datetime
from bs4 import BeautifulSoup
from urllib.request import (urlretrieve)
import os
import re
import requests


class SectionDownloader:
    log = {
        'mod': 0,
        'file_path': 0,
        'file': 0,
        'handler': '',
        'logger': ''
    }

    config = {
        'result_path': './result/',
        'css_tree_shaker_path': './tree_shaker.css'
    }

    req = {
        'url': ''
    }

    file = ''

    html_document = {
        'classes': [],
        'styles': [],
    }

    def write_log(self, log_text):
        """ Write log by print() or logger """
        if self.log['mod'] == 0:
            try:
                now_time = datetime.datetime.now()
                print(now_time.strftime("%d.%m.%Y_%H:%M") + " " + log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
        elif self.log['mod'] == 1:
            # Create log_file if not exist.
            if self.log['file'] == 0:
                self.log['file'] = 1
                now_time = datetime.datetime.now()
                self.log['full_path'] = '%s%s_%s.log' % (
                    self.log['file_path'], self.user_login,
                    now_time.strftime("%d.%m.%Y_%H:%M"))
                formatter = logging.Formatter('%(asctime)s - %(name)s '
                                              '- %(message)s')
                self.log['logger'] = logging.getLogger(self.user_login)
                self.log['handler'] = logging.FileHandler(self.log['full_path'], mode='w')
                self.log['handler'].setFormatter(formatter)
                self.log['logger'].setLevel(level=logging.INFO)
                self.log['logger'].addHandler(self.log['handler'])
            # Log to log file.
            try:
                self.log['logger'].info(log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")

    def set_url(self, url):
        self.req['url'] = url

    def set_file(self, file_path):
        f = open(file_path, 'r')
        self.file = f.read()

    def download_images(self):
        soup = BeautifulSoup(self.file, 'html.parser')
        for image in soup.findAll("img"):
            self.download(image['src'])

    def download(self, url):
        name = url.split("/")[-1]
        path = url.replace(name, '')
        os.makedirs(self.config['result_path'] + path, exist_ok=True)
        self.write_log('Downloading: ' + url[1:])
        if url.lower().startswith("http"):
            urlretrieve(url, self.config['result_path'] + url[1:])
        else:
            urlretrieve(self.req['url'] + url, self.config['result_path'] + url[1:])

    def download_links(self):
        response = requests.get(self.req['url'])
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.findAll('link', href=True):
            if re.search(".css", link['href']):
                self.html_document['styles'].append(self.config['result_path'] + link['href'].replace('./', ''))
                self.download(link['href'])

    def find_styles_by_class_and_append(self, target_path, selector='.container'):
        file = open(self.config['css_tree_shaker_path'], 'a')
        import cssutils
        statement = ''
        sheet = cssutils.parseFile(target_path)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                if selector in rule.selectorText:
                    statement += rule.selectorText
                    statement += '{'
                    for css_property in rule.style:
                        statement += css_property.name + ":" + css_property.value + ";"
                    statement += '}'
                    file.write(statement)
        file.close()

    def tree_shaker_by_class(self):
        for file_path in self.html_document['styles']:
            for element_class in self.html_document['classes']:
                print(element_class)
                self.find_styles_by_class_and_append(file_path, element_class)

    def find_classes(self):
        soup = BeautifulSoup(self.file, 'html.parser')
        classes = []
        for element in soup.find_all(class_=True):
            classes.extend(element["class"])
        self.html_document['classes'] = classes

    def set_css_files(self):
        self.html_document['styles'] = ['/home/ali/Github/version31/section_downloader/result/assets/css/theme.css']
