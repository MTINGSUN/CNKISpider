import scrapy  
from scrapy.crawler import CrawlerProcess  
from scrapy.utils.project import get_project_settings
from CNKISpider.spiders.CN import CnSpider
# from CNKISpider.spiders.ProxiesSpider import ProxiesSpider

process = CrawlerProcess(get_project_settings())  

# process.crawl(ProxiesSpider)
process.crawl(CnSpider)  
process.start() # the script will block here until the crawling is finished  