#!/usr/bin/python
# -*- coding: utf-8 -*-


import data
import sys


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	dates = data.dates()

	d1 = data.load_date(dates.pop(0))

	for date in dates:
		d2 = data.load_date(date)

		cnt, dec_cnt, inc_cnt, pc_avg, pcs = data.compare(d1, d2)

		print '%s;%.2f' % (date, pc_avg)

if __name__ == '__main__':
	main()
