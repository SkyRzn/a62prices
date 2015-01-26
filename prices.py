#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests, re, json, time, os, sys, data
from lxml import html


reload(sys)
sys.setdefaultencoding('utf8')


def parse_page(url, res):
	sys.stdout.write('.')
	sys.stdout.flush()
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
		art = product.find_class('art')[0].text
		art = int(re.search('[0-9]+', art).group())
		
		price = product.find_class('price-new')
		action = bool(price)
		if price:
			price = price[0]
		else:
			price = product.find_class('price')[0]
			
		try:
			price = float(price.text.strip().replace(' ', ''))
		except:
			print '\n!!!\nPrice error! (%s)\n!!!\n', price.text
			return

		presence = bool(product.find_class('quantity yes'))
		
		res[art] = (name, price, presence, action)
		
	
	links = page.find_class('links')[0]
	pageLinks = links.findall('a')
	for pl in pageLinks:
		if pl.text == '>':
			parse_page(pl.values()[0], res)
			return		

def get_prices(key, id, name):
	url = 'http://assorti62.ru/index.php?route=product/category&path=%d&limit=25' % (id)

	print name,
	sys.stdout.flush()

	res = {}
	parse_page(url, res)
	
	print 'ok'

	date = time.strftime('%y.%m.%d')
	
	try:
		os.mkdir(date)
	except:
		pass
	
	f = open('%s/%s.json' % (date, key), 'w')
	text = json.dumps(res)
	f.write(text)
	f.close
	
	return None

def main():
	for key, val in data.parts.items():
		id, name = val
		get_prices(key, id, name)

if __name__ == '__main__':
	main()




