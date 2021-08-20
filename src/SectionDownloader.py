import datetime
import logging


class SectionDownloader:
    log = {
        'mod': 0,
        'file_path': 0,
        'file': 0,
        'handler': '',
        'logger': ''
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
