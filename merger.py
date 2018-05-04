# coding: utf-8
"""
Merge the data sets into one big panel.

Yuhao Zhu

20170407: Merge all data set together and delete the empty rows.
20170423: Revise some typos.
"""

import csv
import os
import datetime
import pandas as pd

path = os.getcwd()

row_name=[u'行政区', u'电子监管号', u'项目名称', u'项目位置', u'面积(公顷)', u'土地来源',
                      u'土地用途', u'供地方式', u'土地使用年限', u'行业分类', u'土地级别', u'成交价格(万元)',
                      u'土地使用权人', u'约定容积率下限', u'约定容积率上限', u'约定交地时间', u'约定开工时间',
                      u'约定竣工时间', u'实际开工时间', u'实际竣工时间', u'批准单位', u'合同签订日期']
row_name_small = [u'行政区', u'面积(公顷)', u'土地使用年限', u'成交价格(万元)', u'约定容积率下限', u'约定容积率上限',
                   u'合同签订日期']
# path is "landchina/year/month/day.csv"
write_file_name = 'landchina/landchina_2013_2016.csv'
write_file = open(write_file_name, 'w', newline='', encoding='utf-8-sig')
writer = csv.writer(write_file)
writer.writerow([name for name in row_name])

write_file_small_name = 'landchina/landchina_2013_2016_small.csv'
write_file_small = open(write_file_small_name, 'w', newline='', encoding='utf-8-sig')
writer_small = csv.writer(write_file_small)
writer_small.writerow([name for name in row_name_small])

for year in range(2013, 2017):
    for month in range(1, 13):
        date = datetime.date(year, month, 1) # The date of the first day of a certain month.
        try:    
            date_next = datetime.date(date.year, date.month + 1, date.day) # The date of the first day of next month.
        except:
            date_next = datetime.date(date.year + 1, 1, date.day)  
        date_distance = (date_next - date).days # How many days in between.
        for day in range(1, date_distance + 1):
            date = datetime.date(year, month, day)
            print('Merge the data for date {}.'.format(date))
            read_file_name = '{0}/landchina/{1}/{2}/{3}.csv'.format(path,
                                                                    datetime.datetime.strftime(date,'%Y'),
                                                                    datetime.datetime.strftime(date,'%m'),
                                                                    datetime.datetime.strftime(date,'%d'))
            read_file = open(read_file_name, 'r', encoding='utf-8-sig')
            reader = csv.reader(read_file)
            for row in reader:
                if row:
                    if row[0] != u'行政区' and row[0] != '':
                        row[0] = row[0].replace(u'本级', '')
                        if row[5] == '0.000000':
                            row[5] = u'新增建设用地'
                        elif row[4] == row[5]:
                            row[5] = u'现有建设用地'
                        else:
                            row[5] = u'新增建设用地(来自存量库)'
                        # Format number
                        try: row[4] = float(row[4])
                        except: pass
                        try: row[8] = int(row[8])
                        except: pass
                        try: row[11] = float(row[11])
                        except: pass
                        try: row[13] = float(row[13])
                        except: pass
                        try: row[14] = float(row[14])
                        except: pass
                        # Format date
                        try: row[15] = datetime.datetime.strptime(row[15], '%Y年%m月%d日').date()
                        except: pass
                        try: row[16] = datetime.datetime.strptime(row[16], '%Y年%m月%d日').date()
                        except: pass
                        try: row[17] = datetime.datetime.strptime(row[17], '%Y年%m月%d日').date()
                        except: pass
                        try: row[21] = datetime.datetime.strptime(row[21], '%Y年%m月%d日').date()
                        except: pass
                        writer.writerow(row)
                        writer_small.writerow([row[0], row[4], row[8], row[11], row[13], row[14], row[21]])
            read_file.close()
write_file.close()

df = pd.read_csv(write_file_name, encoding='utf-8-sig')
print(df.head())

df_small = pd.read_csv(write_file_small_name, encoding='utf-8-sig')
print(df.head())