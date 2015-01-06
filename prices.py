#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests, re, json, time, os
from lxml import html


	#res = {}
	#trs = re.findall('<tr>.*?</tr>', table)
	#for tr in trs:
		#try:
			#art = int(re.findall('\(.*?\:([0-9]*)\)', tr)[0])
			#name = re.findall('<a.*?>(.*?)</a>', tr)[0].strip()
			#price = re.findall('<nobr>(.*?)</nobr>', tr)[0].strip()
			#price = float(price.split(' ')[0])
			#presence = re.findall('<div style=\'color:(.*?);', tr)[0].strip() == 'green'
		#except:
			#print 'String parsing error!'
			#return None
		#res[art] = (name, price, presence)
	#return res


def parse_page(url, res):
	print '.'
	try:
		page = html.parse(url)
		page = page.getroot()
	except:
		print 'Parsing error!'
		return

	products = page.find_class('product-grid')[0].findall('div')
	
	products = filter(lambda x: not x.keys(), products)
	
	for product in products:
		name =  product.find_class('name')[0].find('a').text
		#print name
		art = product.find_class('art')[0].text
		art = int(re.search('[0-9]+', art).group())
		#print art
		
		price = product.find_class('price-new')
		action = bool(price)
		if price:
			price = price[0]
		else:
			price = product.find_class('price')[0]
			
		try:
			price = float(price.text.strip().replace(' ', ''))
		except:
			print 'Price error! (%s)', price.text
			return

		presence = bool(product.find_class('quantity yes'))
		
		res[art] = (name, price, presence, action)
		
	
	links = page.find_class('links')[0]
	pageLinks = links.findall('a')
	for pl in pageLinks:
		if pl.text == '>':
			parse_page(pl.values()[0], res)
			return		

def get_prices(name, path):
	url = 'http://assorti62.ru/index.php?route=product/category&path=%d&limit=25' % (path)

	print '%s loading' % (name)

	res = {}
	parse_page(url, res)
	
	print '\nok'

	date = time.strftime('%y.%m.%d')
	
	try:
		os.mkdir(date)
	except:
		pass
	
	f = open('%s/%s.json' % (date, name), 'w')
	text = json.dumps(res)
	f.write(text)
	f.close
	
	return None
	

get_prices('meat', 25)
get_prices('milk', 17)
get_prices('fish', 57)
get_prices('frozen', 33)
get_prices('vegetables', 60)
get_prices('grocery', 59) #Bakaleya
get_prices('preserves', 169)
### from 22.08.14
get_prices('alco_tabacco', 20)
get_prices('water_coke', 18)
get_prices('tea', 176)
get_prices('confection', 183)
get_prices('bread', 24)
get_prices('cooking', 34)
get_prices('children', 62)






