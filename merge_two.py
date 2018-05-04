# -*- coding: utf-8 -*-
"""
Combine all files of chinaland together into a big data set.
And create a matchbook.

author:
Yuhao Zhu

version:
20170302: Create the file
"""

import csv
import re
import pandas
import os
import datetime

wp = os.getcwd()

df_book = pandas.read_csv("match_book/match_book.csv", encoding='utf-8-sig')
df_landchina = pandas.read_csv(wp+'/landchina/landchina_2013_2016_small.csv', encoding='utf-8-sig')

df = pandas.merge(df_book, df_landchina, left_on='NAME_3_CHINESE', right_on=u'行政区')
df = df[['NAME_3','面积(公顷)','成交价格(万元)','约定容积率下限','约定容积率上限']]

df.rename(columns = {'面积(公顷)': 'area(hectare)',
                     '成交价格(万元)': 'price(million)',
                     '约定容积率下限': 'ratio_low',
                     '约定容积率上限': 'ratio_high'}, inplace=True)

df_price = df[df['price(million)'] > 0]
df_price = df_price.groupby(['NAME_3'], as_index=False)['price(million)'].sum()
df_price.to_csv('price.csv', encoding='utf-8-sig')