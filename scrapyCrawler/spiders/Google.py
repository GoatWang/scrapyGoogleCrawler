from bs4 import BeautifulSoup
import scrapy
from .setting_selenium import cross_selenium
from scrapyCrawler.items import ScrapycrawlerItem
from .preprocessing import preprocessing
import datetime
import re

class Googlespider(scrapy.Spider):
    name = 'Google'
    start_urls = ['https://www.google.com.hk/webhp?hl=en-us']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36','referer':'https://www.google.com.hk/webhp?hl=en-us'}
    target_corp_info = ""
    def __init__(self, finding_corps=None, target_corp=None, *args, **kwargs):
        super(Googlespider, self).__init__(*args, **kwargs)
        self.target_corp = target_corp
        # self.finding_corp = finding_corp
        self.finding_corps = eval(finding_corps)

    def start_requests(self):
        for corp in self.finding_corps:
            path = self.start_urls[0]     
            driver = cross_selenium()
            driver.get(path)
            elem = driver.find_element_by_css_selector('.lst')
            elem.send_keys(corp + ' product')
            elem.submit()
            html = driver.page_source
            driver.close()

            soup = BeautifulSoup(html, 'lxml')
            for link in soup.find_all('a'):
                if "/url?q=" in str(link) and not 'googleusercontent' in str(link):
                    url = link['href'].split('&sa')[0].replace('/url?q=', '')
                    if re.findall(r'^http', url.lower()):
                        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, meta={'corp':corp})
                    
    def parse(self, response):
        contype = response.headers[b'Content-Type']
        if not 'text/html' in str(contype):
            print(response.url, contype)


        html = response.body
        soup = BeautifulSoup(html ,'lxml')
        [x.extract() for x in soup.findAll('script')]
        [x.extract() for x in soup.findAll('style')]
        [x.extract() for x in soup.findAll('nav')]
        [x.extract() for x in soup.findAll('footer')]

        corpInfoItem = ScrapycrawlerItem()
        corpInfoItem['target_corp'] = self.target_corp
        corpInfoItem['finding_corp'] = response.meta['corp']
        corpInfoItem['url'] = response.url
        corpInfoItem['info'] = preprocessing(soup.text)
        corpInfoItem['crawling_time'] = datetime.datetime.utcnow()

        yield corpInfoItem

    
