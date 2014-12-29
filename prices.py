#!/usr/bin/python


import requests, re, json, time, os


def parse_table(table):
	res = {}
	trs = re.findall('<tr>.*?</tr>', table)
	for tr in trs:
		try:
			art = int(re.findall('\(.*?\:([0-9]*)\)', tr)[0])
			name = re.findall('<a.*?>(.*?)</a>', tr)[0].strip()
			price = re.findall('<nobr>(.*?)</nobr>', tr)[0].strip()
			price = float(price.split(' ')[0])
			presence = re.findall('<div style=\'color:(.*?);', tr)[0].strip() == 'green'
		except:
			print 'String parsing error!'
			return None
		res[art] = (name, price, presence)
	return res

def get_prices(name, path):
	url = 'http://assorti62.ru/index.php?route=product/category&path=%d&limit=25' % (path)

	r = requests.get(url)
	if r.status_code != 200:
		print 'Bad status code!'
		return None
	
	content = r.text.replace('\n', '')
	
	try:
		table = re.findall('<tbody>.*?</table>', content)[0]
	except:
		print 'Table finding error!'
		return None

	try:
		links = re.findall('<div class="links">(.*?)</div>', content)[0]
		max_page = int(re.findall('<a.*?>(.*?)</a>', links)[-1])
	except:
		print 'Max page not found!'
		return None
	print 'Downloading table "%s"? %d pages' % (name, max_page)
	
	res = parse_table(table)
	if not res:
		print 'Parse error!'
		return None
	
	print '\t1'
	
	for page in range(2, max_page + 1):
		url2 = '%s&page=%d' % (url, page)
		r = requests.get(url2)
		if r.status_code != 200:
			print 'Bad status code on page %d!' % (page)
			return None
		
		content = r.text.replace('\n', '')
			
		try:
			table = re.findall('<tbody>.*?</table>', content)[0]
		except:
			print 'Table finding error on page %d!' % (page)
			return None
		
		res.update(parse_table(table))
		if not res:
			print 'Parse error on page %d!' % (page)
			return None
		print '\t%d' % (page)

	date = time.strftime('%y.%m.%d')
	
	try:
		os.mkdir(date)
	except:
		pass
	
	f = open('%s/%s.json' % (date, name), 'w')
	text = json.dumps(res)
	f.write(text)
	f.close
	

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






