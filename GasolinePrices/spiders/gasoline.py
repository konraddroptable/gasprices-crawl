import scrapy
import re
from GasolinePrices.items import GasolinePricesItem
import datetime


class GasolineSpider(scrapy.Spider):
    name = "Gasoline"
    allowed_domains = ["cenapaliw.pl"]
    start_urls = [ \
        "https://www.cenapaliw.pl/?o=&m=95", \
        "https://www.cenapaliw.pl/?o=&m=98", \
        "https://www.cenapaliw.pl/?o=&m=d", \
        "https://www.cenapaliw.pl/?o=&m=e"]
    
    def parse(self, response):
        for href in response.xpath("//table[@id='priserna']/tr[last()-1]/td/a/@href").extract():
            url = response.urljoin(response.url.split('?')[0] + href)
            yield scrapy.Request(url, callback=self.parse)
        
        item = GasolinePricesItem()
        gas = response.xpath("//table[@id='priserna']/tr[1]/td[3]/b/text()").extract()[0]
        
        for i in range(2, len(response.xpath("//table[@id='priserna']/tr")) - 1):
            item["company"] = self.parseText(response.xpath(self.mergePath("//table[@id='priserna']/tr[",i,"]/td[@class='texttab'][1]/text()")).extract()[0])
            item["address"] = self.parseText(response.xpath(self.mergePath("//table[@id='priserna']/tr[",i,"]/td[@class='texttab']//a/text()")).extract()[0])
            item["city"] = self.parseText(response.xpath(self.mergePath("//table[@id='priserna']/tr[",i,"]/td[@class='texttab'][4]/text()")).extract()[0])
            item["price"] = self.getPrice(response.xpath(self.mergePath("//table[@id='priserna']/tr[",i,"]/td//span[@class='c2a']/text()")).extract()[0])
            item["updated"] = self.getUpdateDate(response.xpath(self.mergePath("//table[@id='priserna']/tr[",i,"]/td//span[@class='c2a']/text()")).extract()[0])
            item["gasType"] = self.parseText(gas)
            item["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:00')
            yield item

    def getPrice(self, x):
        s = re.findall(r'[0-9]\,[0-9]{1,2}', x)
        if len(s) > 0:
            return s[0]
        else:
            return 'NA'
    
    def getUpdateDate(self, x):
        s = re.findall(r'\([0-9]{1,2}\/[0-9]{1,2}\)', x)
        if len(s) > 0:
            d = int(re.sub(u'\(', '', re.findall('\([0-9]{1,2}', s[0])[0]))
            m = int(re.sub(u'\)', '', re.findall('[0-9]{1,2}\)', s[0])[0]))
            y = datetime.date.today().year
            return datetime.date(y, m, d)
        else:
            return 'NA'
    
    def parseText(self, x):
        return re.sub(r'^ +| +$', '', x)
        
    def mergePath(self, s1, i, s2):
        return str(s1) + str(i) + str(s2)    