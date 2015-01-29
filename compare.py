#!/usr/bin/python
# -*- coding: utf-8 -*-


import data
import sys


filters = { 'молоко': ur'^молоко(?!.*чудо|.*сгущенное|.*детское)',
			'сосиски': ur'сосиски',
			'пельмени': ur'пельмени',
			'гречка': ur'крупа гречневая|греча',
			'рис': ur'^рис',
			'макароны': ur'^макарон(?!.*по-флотски)',
			'масло сливочное': ur'^масло(?=.*сливочное)',
			'масло подсолнечное': ur'^масло(?=.*подсолнечное)',
			'тушенка': ur'^свинина|^говядина(?=.*тушеная)',
			'яблоки': ur'яблоки',
			'апельсины': ur'апельсины',
			'сахар': ur'^сахар(?!.*пудра)',
			'соль': ur'^соль(?!.*морская)',
			'яйца': ur'^яйцо куриное',
			'сыр': ur'^сыр (?!.*плавл|.*президент|.*хохланд|.*копченый|.*сырцееды|.*каймак)',
			'сыр плавленный': ur'^сыр (?=.*плавл)',
			'сметана': ur'^сметана',
			'водка': ur'водка',
			'пиво': ur'пиво',
			'хлеб': ur'^хлеб |батон ',
			'лук': ur'^лук',
			'морковь': ur'^морковь',
			'капуста': ur'^капуста(?=.*бел)',
			'яблоки': ur'яблоки',
			}


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	by_cat = False
	flt = None

	args = sys.argv[1:]
	while args:
		arg = args.pop(0)
		if arg.startswith('--'):
			arg = arg[2:]
			if arg == 'bycat':
				by_cat = True
			if arg == 'filter':
				flt = args.pop(0)
				flt = filters.get(flt, ur'%s' % flt)
			else:
				raise Exception('Unknown arg')

	dates = data.dates()

	d1 = data.load_date(dates[0])
	d2 = data.load_date(dates[-1])

	if by_cat:
		for cat, val in data.categories.items():
			n, name = val
			cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2, flt, [cat])
			print '%s - %6.2f%%' % (name, pc_avg)
		return

	if flt == 'all':
		for name, fl in filters.items():
			cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2, fl)
			print '%s - %6.2f%%' % (name, pc_avg)
		return

	cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2, flt)

	pcs.sort()

	for percent, name, price1, price2, act1, act2 in pcs:
		two_pr = True
		if price1 > price2:
			fmt = '\033[1;32m%-50.50s\t%6.2f%%\033[0m %s'
		elif price1 < price2:
			fmt = '\033[0;31m%-50.50s\t%6.2f%%\033[0m %s'
		else:
			fmt = '%-50.50s\t%6.2f%% %s'
			two_pr = False

		sact = ''
		if act1 != act2:
			sact = 'акция (%s)' % ('начало' if act1 else 'конец')

		print fmt % (name, percent, '%7.2f -> %7.2f %s' % (price1, price2, sact))

	print
	print 'подорожало %d, подешевело %d из %d, среднее: %6.2f%%' % (inc_cnt, dec_cnt, cnt, pc_avg)

if __name__ == '__main__':
	main()
