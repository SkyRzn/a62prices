#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests, re, json, time, os, sys


nocolor = ('--nocolor' in sys.argv)


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
		#if 'children' in fn or 'water' in fn or 'alco' in fn:
			#continue
		#if 'vegeta' not in fn:
			#continue
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
			if presence:
				item[1].append(price)
				item[2].append(presence)
				item[3].append(date)
		#else:
			#item[2].append(False)

print '\n-------------------- price changed'
n = 0
alln = 0
incn = 0
decn = 0
avg = 0
appeared = []
disappeared = []
prch = []
for key, val in items.items():
	name, prices, presences, dates = val
	if len(prices) > 0:
		alln += 1
		if True in presences:
			if prices[-1] > prices[0]:
				incn += 1
			if prices[-1] < prices[0]:
				decn += 1
			n += 1
			avg += float(prices[-1])/prices[0]*100
			prc = prices[-1]/prices[0]*100

			if prc == 100:
				fmt = '%s\t%-50.50s\t%s'
			elif prc < 100:
				fmt = '%s\t%-50.50s\t%s' if nocolor else '%s\t\033[1;32m%-50.50s\t%s\033[0m'
			else:
				fmt = '%s\t%-50.50s\t%s' if nocolor else '%s\t\033[0;31m%-50.50s\t%s\033[0m'

			#if presences[-1] and not presences[0]:
				#fmt = '\033[1;32m+\033[0m' + fmt
			#elif not presences[-1] and presences[0]:
				#fmt = '\033[1;31m-\033[0m' + fmt
			#else:
				#fmt = ' ' + fmt

			prcs = []
			for i, price in enumerate(prices):
				if i == 0 or i == len(prices) - 1:
					if presences[i]:
						prcs.append('%.2f (%.2f) (%s)' % (float(price)/prices[0]*100, price, dates[i]))
					else:
						prcs.append('-%.2f' % (float(price)/prices[0]*100))
			prcs = '\t'.join(prcs)

			prch.append((prc, fmt % (key, name, prcs), key))

prch.sort()
for p in prch:
	prc, s, key = p

	#if int(key) in [8056, 29410, 41050, 27724, 35655, 30160, 21481, 201386]:
	if prc != 100:
		print s

if n:
	print 'подорожало %d, подешевело %d из %d, среднее: %.2f%%' % (incn, decn, alln, avg/n)
else:
	print '%d from %d' % (incn, alln)


def print_presence():
	print '\n-------------------- presence changed'
	for key, val in items.items():
		name, prices, presences = val
		if presences[0] != presences[-1]:
			if presences[-1]:
				print '%s \033[1;32m%-32s\t%s\033[0m' % (key, name, prices[-1])
			else:
				print '%s \033[1;31m%-32s\t%s\033[0m' % (key, name, prices[-1])




def lol():
	print len(arts)

	beg = res[dates[0]]
	end = res[dates[-1]]

	price_changed = {}
	disappeared = {}
	appeared = {}

	for key, val in beg.items():
		name, price, presence = val

		try:
			nname, nprice, npresence = end[key]
		except:
			disappeared[key] = (name, price)
			continue

		if nprice != price:
			price_changed[key] = (name, nprice/price*100)
		if presence and not npresence:
			disappeared[key] = (name, price)
		if npresence and not presence:
			appeared[key] = (name, price)

	print '\n-------------------- price changed'
	for key, val in price_changed.items():
		name, prc = val
		if nocolor:
			fmt = '%s\t%-32s\t%s' if prc <= 100 else '%s\t%-32s\t%s'
		else:
			fmt = '%s\t\033[1;32m%-32s\t%s\033[0m' if prc <= 100 else '%s\t\033[1;31m%-32s\t%s\033[0m'
		print fmt % (key, name, prc)

	print '\n-------------------- disappeared'
	for key, val in disappeared.items():
		name, price = val
		print '%s \033[1;31m%-32s\t%s\033[0m' % (key, name, price)

	print '\n-------------------- appeared'
	for key, val in appeared.items():
		name, price = val
		print '%s \033[1;32m%-32s\t%s\033[0m' % (key, name, price)
