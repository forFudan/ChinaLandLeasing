# -*- coding: utf-8 -*-
"""
This file transfer the 4-digit code into Chinese characters.
And create a matchbook.

author:
Yuhao Zhu

version:
20170302: Create the file.
"""

import csv
import re
import pandas

# Level 1 name
match_book_csv_file = open('match_book_level_3.csv', 'w', encoding='utf-8-sig')
match_book_writer = csv.writer(match_book_csv_file)

adm_csv_file = open('CHN_adm3.csv', 'r', encoding='utf-8-sig')
adm_csv_reader = csv.reader(adm_csv_file)

head_line = ['ID_1', 'NAME_1', 'ID_2', 'NAME_2', 'ID_3', 'NAME_3', 'NAME_3_CHINESE']
match_book_writer.writerow(head_line)
for row in adm_csv_reader:
    if row[5] != 'NAME_1':
        chinese = row[14].split('|')
        if len(chinese) == 2:
            chinese = chinese[1]
        else:
            chinese = chinese[0]
        codes = re.findall(r'<U\+(.*?)>', chinese)
        characters = []
        for code in codes:
            code = '\\u{}'.format(code)
            code = code.encode('ascii')
            code = code.decode('unicode-escape')
            characters.append(code)
        place = ''.join(characters)
        row[14] = place
        matching = [row[4], row[5], row[6], row[7], row[8], row[9], place]
        match_book_writer.writerow(matching)
match_book_csv_file.close()

# Level 2 name
match_book_csv_file = open('match_book_level_2.csv', 'w', encoding='utf-8-sig')
match_book_writer = csv.writer(match_book_csv_file)

adm_csv_file = open('CHN_adm2.csv', 'r', encoding='utf-8-sig')
adm_csv_reader = csv.reader(adm_csv_file)

head_line = ['ID_1', 'NAME_1', 'ID_2', 'NAME_2', 'NAME_2_CHINESE']
match_book_writer.writerow(head_line)
for row in adm_csv_reader:
    if row[5] != 'NAME_1':
        chinese = row[13].split('|')
        if len(chinese) == 2:
            chinese = chinese[1]
        else:
            chinese = chinese[0]
        codes = re.findall(r'<U\+(.*?)>', chinese)
        characters = []
        for code in codes:
            code = '\\u{}'.format(code)
            code = code.encode('ascii')
            code = code.decode('unicode-escape')
            characters.append(code)
        place = ''.join(characters)
        row[13] = place
        matching = [row[4], row[5], row[6], row[7], place]
        match_book_writer.writerow(matching)
match_book_csv_file.close()

# Level 3 name
match_book_csv_file = open('match_book_level_1.csv', 'w', encoding='utf-8-sig')
match_book_writer = csv.writer(match_book_csv_file)

adm_csv_file = open('CHN_adm1.csv', 'r', encoding='utf-8-sig')
adm_csv_reader = csv.reader(adm_csv_file)

head_line = ['ID_1', 'NAME_1', 'NAME_1_CHINESE']
match_book_writer.writerow(head_line)
for row in adm_csv_reader:
    if row[5] != 'NAME_1':
        chinese = row[11].split('|')
        if len(chinese) == 2:
            chinese = chinese[1]
        else:
            chinese = chinese[0]
        codes = re.findall(r'<U\+(.*?)>', chinese)
        characters = []
        for code in codes:
            code = '\\u{}'.format(code)
            code = code.encode('ascii')
            code = code.decode('unicode-escape')
            characters.append(code)
        place = ''.join(characters)
        row[11] = place
        matching = [row[4], row[5], place]
        match_book_writer.writerow(matching)
match_book_csv_file.close()

# Combine the match book
df_level_3 = pandas.read_csv('match_book_level_3.csv', encoding='utf-8-sig')
df_level_2 = pandas.read_csv('match_book_level_2.csv', encoding='utf-8-sig')
df_level_1 = pandas.read_csv('match_book_level_1.csv', encoding='utf-8-sig')

df_level_1_2 = pandas.merge(df_level_1, df_level_2, on=['ID_1', 'NAME_1'])
df = pandas.merge(df_level_1_2, df_level_3, on=['ID_1', 'NAME_1', 'ID_2', 'NAME_2'])

print(df.head())
# Fill in the empty names for level 3
mask_1 = pandas.isnull(df['NAME_3_CHINESE']) # Lack county level for city region. Due to change in the name.
# Use City name as county name if it is urban regions.
mask_2 = (df['NAME_3'] == df['NAME_2'])
mask = mask_1 & mask_2

df.loc[mask, 'NAME_3_CHINESE'] = df['NAME_2_CHINESE']
pandas.DataFrame.to_csv(df, 'match_book.csv', encoding='utf-8-sig')