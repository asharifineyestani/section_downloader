from src.SectionDownloader import SectionDownloader

sd = SectionDownloader()
sd.set_file('test.html')
sd.set_url('https://example.com/')
sd.download_images()
sd.download_links()
sd.find_classes()
sd.set_css_files()
sd.tree_shaker_by_class()
