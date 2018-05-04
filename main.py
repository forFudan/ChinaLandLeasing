# coding: utf-8
"""
A downloader that catch the data from Chinese land data website.

Yuhao Zhu

20170224: Creation of the file and adjust the code.
20170225: Create a log file for links that are not able to connect.
"""

import requests, re, os, sys, csv, datetime
sys.path.append(os.getcwd())
import downloader

year = int(sys.argv[1])
month = int(sys.argv[2])
day = int(sys.argv[3])

print("Download from {}/{}/{}.".format(year, month, day))
spider = downloader.Downloader()

spider.land_download(year, month, day)

#for year in range(2014, 2015):
#    for month in range(6, 11):
#        spider.land_download(year, month, 1)