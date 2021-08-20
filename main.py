from src.SectionDownloader import SectionDownloader

sd = SectionDownloader()
sd.set_file('test.html')
sd.set_url('https://google.com/')
sd.download_images()
