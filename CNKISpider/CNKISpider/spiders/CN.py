# -*- coding: utf-8 -*-
import scrapy
import re
import time
from CNKISpider.items import CnkispiderItem
import urllib.request
from urllib.error import URLError
from lxml import etree


class CnSpider(scrapy.Spider):
    name = 'CN'
    allowed_domains = ['search.cnki.com.cn']
    start_urls = ['http://search.cnki.com.cn/Search.aspx?q=%e8%87%aa%e7%84%b6%e8%af%ad%e8%a8%80%e5%a4%84%e7%90%86&rank=citeNumber&cluster=all&val=&p=0',
                 ]

    # task_urls = []
    # # 虽然显示有14729条记录，实际只能显示到67页
    # # 尝试使scrapy框架按顺序爬取
    # for i in range(0, 70):
    #     task_url = 'http://search.cnki.com.cn/Search.aspx?q=%e8%87%aa%e7%84%b6%e8%af%ad%e8%a8%80%e5%a4%84%e7%90%86&rank=citeNumber&cluster=all&val=&p='+ str(15*i)
    #     task_urls.append(task_url)
    # print('共爬取',len(task_urls),'页')

    def parse(self, response):
    	# while response.status != 200:
    	# 	print('*****************',response.url,'访问失败，重新尝试。**************')
    	# 	return scrapy.Request(url = response.url, callback=self.parse)   
    	urls = []
    	print('\n\n****************爬取resposne.url: ', response.url ,' **************************')
    	# 下一页url
    	try:
    		url = response.xpath('.//*[@id="page"]/a[11]/@href').extract()[0]
    	except:
    		url = response.xpath('.//*[@id="page"]/a[10]/@href').extract()[0]
    	url_1 = 'http://search.cnki.com.cn/'
    	task_url = 	url_1 + url
    	print('****************爬取task_url: ', task_url ,' **************************')
    	time.sleep(1)

    	contents = response.xpath('.//div[@class="wz_content"]').extract()
    	print('\n获取到contents:',len(contents),'条数据')
    	first_url = re.findall('href="(.*?)"', contents[0])[0]
    	print('FIRST URL:', first_url)

    	last_url = re.findall('href="(.*?)"', contents[-1])[0]
    	print('LAST CONTENT:', last_url)
    	time.sleep(1)

    	i = 0
    	for content in contents:
    		i = i + 1
    		print('\n********************第',i,'个content**********************')
    		
    		item = CnkispiderItem()

    		# 删去源代码中例如关键词“<span class="red_text">自然语言处理</span>”的标签
    		content = content.replace('<span class="red_title">自然</span>','自然')
    		content = content.replace('<span class="red_title">语言</span>','语言')
    		content = content.replace('<span class="red_title">处理</span>','处理')    
    		content = content.replace('<span class="red_title">自然语言</span>','自然语言')
    		content = content.replace('<span class="red_text">自然语言处理</span>','自然语言处理')
    		content = content.replace('<span class="red_title"><span class="red_title">自然语言处理</span></span>','自然语言处理')      
    		print('********************数据清理完毕*****************************')
    		
    		# 解析url信息
    		url = re.findall('<a href="(.*?)"',content)[0]
    		print('URL:', url)
    		urls.append(url)

    		# 解析title信息
    		title = re.findall('target="_blank">(.*?)</a>',content)[0]
    		print('TITLE:', title)
    		

    		# 解析下载数信息
    		download_num = re.findall('<span class="count">下载次数（(.*?)）',content)[0]
    		print('download_num:',download_num)

    		# 解析被引量信息
    		reference_num = re.findall('被引次数（(.*?)）',content)[0]
    		print('reference_num:',reference_num)

    		# 解析期刊信息
    		journal = re.findall('<span title="(.*?)">', content)[0]
    		print('journal:',journal)
    		time.sleep(1)

    		# 解析出版年信息
    		try:
    			year = re.findall('(\d{4})年', content)[0]
    			print('year:',year)
    			time.sleep(1)
    		except:
    			year = re.findall('(\d{4})-', content)[0]
    			print('year:',year)
    			time.sleep(1)
    		
    		# 打开抓取的URL，获取完整的摘要、作者、作者单位和基金信息
    		# 会出现重定向死循环问题

    		try:
    			print('————————————urllib.request.urlopen', url,'——————————————')
    			html = urllib.request.urlopen(url).read()
    			selector=etree.HTML(html)

    			abstract = selector.xpath(".//*[@id='content']/div[2]/div[4]/text()")[-1]
    			print('abstract:',abstract[:5])
    			time.sleep(1)

    			authors = selector.xpath(".//*[@id='content']/div[2]/div[3]/a/text()")# list类型 
    			# 将list转化为sting，元素用,隔开
    			authors = ",".join(str(a) for a in authors)
    			print('Authors:', authors)

    			organizations = selector.xpath(".//*[@id='content']/div[2]/div[5]/a[1]/text()")
    			if len(organizations) != 0:
    				organizations = ",".join(str(o) for o in organizations)
    				print('Organizations:', organizations)
    			else:
    				organizations = None
    				print('Organizations:', organizations)

    			funds = selector.xpath(".//*[@id='content']/div[2]/div[5]/a[2]/text()")
    			if len(funds) != 0:
    				funds = ",".join(str(f) for f in funds)
    				print('Funds:', funds)
    			else:
    				funds = None
    				print('Funds: ', funds)
    				time.sleep(1)

    		except URLError as e:
    			if hasattr(e, 'reason'):
    				print('\n\n——————————————We failed to reach a server.——————————————')
    				print('Reason: ', e.reason)
    			elif hasattr(e, 'code'):
    				print('\n\n——————————————The server couldn\'t fulfill the request.——————————————')
    				print('Error code: ', e.code)
    		else:
    			print('————————————————everything is fine——————————————')

    		item['url'] = url
    		item['title'] = title
    		item['authors'] = authors
    		item['organizations'] = organizations
    		item['funds'] = funds
    		item['abstract'] = abstract
    		item['download_num'] = download_num
    		item['reference_num'] = reference_num
    		item['journal'] = journal
    		item['year'] = year

    		yield item
    	print('解析得到urls:',len(urls),'条数据')

    	# count = len(self.task_urls) - 1
    	# if count != 0:
    	# 	print('剩余', count, '个页面\n')
    	# 	if first_url == urls[0] and last_url == urls[-1]:
    	# 		self.task_urls.remove(response.url)
    	# 		print('\n\n**************task_urls[0]:', self.task_urls[0],'****************')
    	# 		yield scrapy.Request(url=self.task_urls[0], callback=self.parse)
    	# else:
    	# 	print('\n************************无更多任务*****************************')

    	if response.url != task_url:
    		yield scrapy.Request(url=task_url, callback=self.parse)
    	else:
    		print('\n************************无更多任务*****************************')






