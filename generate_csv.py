#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests, re, json, time, os


parts = {'alco_tabacco.json': 'алкоголь/табак',
			'bread.json': 'хлеб',
			'children.json': 'детские товары',
			'confection.json': 'кондитерские изделия',
			'cooking.json': 'кулинария',
			'fish.json': 'рыба и морепродукты',
			'frozen.json': 'замороженные продукты',
			'grocery.json': 'бакалея',
			'meat.json': 'мясо и мясопродукты',
			'milk.json': 'молоко и молочные продукты',
			'preserves.json': 'консервы',
			'tea.json': 'чай/кофе',
			'vegetables.json': 'овощи, фрукты, грибы',
			'water_coke.json': 'вода, напитки, соки'}
 
res = {}

for top, dirs, files in os.walk('.'):
	date = top[2:]
	if not date:
		continue
	
	
	files = filter(lambda x: x.endswith('.json'), files)
	
	day = {}

	for fn in files:
		f = open('%s/%s' % (date, fn), 'r')
		j = json.loads(f.read())
		f.close()
		
		day.update(j)
	res[date] = day
	
dates = res.keys()
dates.sort()

items = {}

for date in dates:
	for key, val in res[date].items():
		items[key] = (val[0], [], [], [])


for itkey, item in items.items():
	for date in dates:
		if itkey in res[date]:
			name, price, presence = res[date][itkey]
			item[1].append(price)
			item[2].append(presence)
			item[3].append(date)
		else:
			item[2].append(False)


res = []

row = 'Арт.;Наименование;'
for date in dates:
	row += '%s;' % date
res.append(row.decode('UTF-8'))

rows = []

for key, val in items.items():
	name, prices, presences, curDates = val
	name = name.replace(';', ',')

	row = '%s;%s;' % (key, name)

	firstValue = 0
	lastValue = 0
	for date in dates:
		if date in curDates:
			i = curDates.index(date)
			if presences[i]:
				lastValue = float(prices[i])
				if not firstValue:
					firstValue = float(prices[i])

	if firstValue and lastValue:
		for date in dates:
			if date in curDates:
				i = curDates.index(date)
				if prices[0] == 0:
					row += '0'
				else:
					prc = float(prices[i])/firstValue*100
					row += '%.2f%%' % (prc)
				if presences[i]:
					row += ' (+);'
				else:
					row += ' (-);'
			else:
				row += ' - ;'
		rows.append((lastValue/firstValue, row))

rows.sort()
for pr, val in rows:
	res.append(val)

f = open('prices_19.08.14-29.08.14.csv', 'w')
s = '\n'.join(res)
f.write(s.encode('UTF-8'))
f.close()


