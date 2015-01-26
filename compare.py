#!/usr/bin/python
# -*- coding: utf-8 -*-


import data
import sys


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	dates = data.dates()

	d1 = data.load_date(dates[0])
	d2 = data.load_date(dates[-1])

	flt = ur'^молоко(?!.*чудо|.*сгущенное|.*детское)' #молоко
	flt = ur'сосиски' #сосиски
	flt = ur'пельмени' #пельмени
	flt = ur'крупа гречневая|греча' #гречка
	flt = ur'^рис' #рис
	flt = ur'^макарон(?!.*по-флотски)' #макароны
	flt = ur'^масло(?=.*сливочное)' #макароны
	flt = ur'^масло(?=.*подсолнечное)' #макароны
	flt = ur'тушен' #макароны
	flt = ur'^свинина|^говядина(?=.*тушеная)' #тушенка
	flt = ur'яблоки' #яблоки
	flt = ur'апельсины' #апельсины
	flt = ur'^сахар(?!.*пудра)' #сахар
	flt = ur'^соль(?!.*морская)' #соль
	flt = ur'^яйцо куриное' #яйца
	flt = ur'^сыр (?=.*плавл)' #сыр плавленный
	flt = ur'^сыр (?!.*плавл|.*президент|.*хохланд|.*копченый|.*сырцееды|.*каймак)' #сыр
	flt = ur'^сметана' #сметана
	flt = ur'водка' #водка
	flt = ur'пиво' #пиво
	flt = ur'^хлеб |батон ' #хлеб

	cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2, flt)

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
