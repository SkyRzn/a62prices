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
			}


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	dates = data.dates()

	d1 = data.load_date(dates[0])
	d2 = data.load_date(dates[-1])

	#for name, flt in filters.items():
		#cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2, flt)
		#print '%s - %6.2f%%' % (name, pc_avg)
	#return

	cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2)

	pcs.sort()

	for percent, name, price1, price2 in pcs:
		two_pr = True
		if percent < 99.9:
			fmt = '\033[1;32m%-50.50s\t%6.2f%%\033[0m %s'
		elif percent > 100.1:
			fmt = '\033[0;31m%-50.50s\t%6.2f%%\033[0m %s'
		else:
			fmt = '%-50.50s\t%6.2f%% %s'
			two_pr = False

		print fmt % (name, percent, '%7.2f -> %7.2f' % (price1, price2))

	print
	print 'подорожало %d, подешевело %d из %d, среднее: %6.2f%%' % (inc_cnt, dec_cnt, cnt, pc_avg)

if __name__ == '__main__':
	main()
