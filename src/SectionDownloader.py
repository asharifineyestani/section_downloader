import logging
import datetime
from bs4 import BeautifulSoup
from urllib.request import (urlretrieve)
import os


class SectionDownloader:
    log = {
        'mod': 0,
        'file_path': 0,
        'file': 0,
        'handler': '',
        'logger': ''
    }

    config = {
        'result_path': './result/'
    }

    req = {
        'url': ''
    }

    file = ''

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
            image["name"] = image["src"].split("/")[-1]
            image['path'] = image["src"].replace(image["name"], '')
            os.makedirs(self.config['result_path'] + image['path'], exist_ok=True)

            self.write_log('Downloading image: ' + image["src"][1:])
            if image["src"].lower().startswith("http"):
                urlretrieve(image["src"], self.config['result_path'] + image["src"][1:])
            else:
                urlretrieve(self.req['url'] + image["src"], self.config['result_path'] + image["src"][1:])
