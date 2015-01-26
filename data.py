#!/usr/bin/python
# -*- coding: utf-8 -*-


import re, json, time, os, sys


nocolor = ('--nocolor' in sys.argv)


parts = {'alco_tabacco': (20 ,'алкоголь/табак'),
			'bread': (24 ,'хлеб'),
			'children': (62 ,'детские товары'),
			'confection': (183 ,'кондитерские изделия'),
			'cooking': (34 ,'кулинария'),
			'fish': (57 ,'рыба и морепродукты'),
			'frozen': (33 ,'замороженные продукты'),
			'grocery': (59 ,'бакалея'),
			'meat': (25 ,'мясо и мясопродукты'),
			'milk': (17 ,'молоко и молочные продукты'),
			'preserves': (169 ,'консервы'),
			'tea': (176 ,'чай/кофе'),
			'vegetables': (60 ,'овощи, фрукты, грибы'),
			'water_coke': (18 ,'вода, напитки, соки')}

def dates():
	root, dirs, files = os.walk('data').next()
	res = []
	for dir in dirs:
		if not re.match('^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$', dir):
			continue
		res.append(dir)
	res.sort()
	return res

def load_date(date):
	root, dirs, files = os.walk('data/%s' % date).next()

	files = filter(lambda x: x.endswith('.json'), files)

	data = {}

	for fn in files:
		f = open('data/%s/%s' % (date, fn), 'r')
		j = json.loads(f.read())
		f.close()

		data.update(j)

	return data

def fix_action(vals):
	if len(vals) == 3:
		name, price, presence = vals
		vals = (name, price, presence, False)
	return vals

def compare(d1, d2, flt = None):
	cnt = dec_cnt = inc_cnt = 0
	percent_sum = 0
	pcs = []
	for id, v1 in d1.items():
		try:
			v2 = d2[id]
		except:
			continue

		name, price1, prs1, act1 = fix_action(v1)
		name, price2, prs2, act2 = fix_action(v2)

		if not (prs1 and prs2):
			continue
		#if act1 or act2:
			#continue

		if flt:
			if not re.search(flt, name.lower()):
				continue

		if price1 > price2:
			dec_cnt += 1
		if price1 < price2:
			inc_cnt += 1
		cnt += 1

		percent = 100.0/float(price1)*float(price2)
		percent_sum += percent

		pcs.append((percent, name, price1, price2))

	percent_avg = 0 if cnt == 0 else percent_sum/float(cnt)

	return (cnt, dec_cnt, inc_cnt, percent_avg, pcs)

