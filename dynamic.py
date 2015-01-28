#!/usr/bin/python
# -*- coding: utf-8 -*-


import data
import sys


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	by_cat = False
	sort = False
	stream = sys.stdout

	args = sys.argv[1:]
	while args:
		arg = args.pop(0)
		if arg.startswith('--'):
			arg = arg[2:]
			if arg == 'bycat':
				by_cat = True
			elif arg == 'file':
				fn = args.pop(0)
				stream = open(fn, 'w')
			elif arg == 'sort':
				sort = True
			else:
				raise Exception('Unknown arg')

	dates = data.dates()

	d1 = data.load_date(dates.pop(0))

	cats = data.categories.keys()

	if by_cat:
		if sort:
			d2 = data.load_date(dates[-1])
			s = []
			for cat in data.categories.keys():
				cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2, cats=[cat])
				s.append((pc_avg, cat))
			s.sort(reverse=True)
			cats = [c for p, c in s]

		s = ['Дата']
		for cat in cats:
			s.append(data.categories[cat][1])
		print >> stream, ';'.join(s)
	else:
		print >> stream, 'Дата;Цена(%)'

	for date in dates:
		d2 = data.load_date(date)

		if by_cat:
			s = [date]
			for cat in cats:
				cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2, cats = [cat])
				s.append('%.2f' % pc_avg)
			print >> stream, ';'.join(s)
		else:
			cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2)
			print >> stream, '%s;%.2f' % (date, pc_avg)

if __name__ == '__main__':
	main()
