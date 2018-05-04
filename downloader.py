# coding: utf-8
"""
A downloader that catch the data from Chinese land data website.

Yuhao Zhu

20170224: Creation of the file and adjust the code.
20170225: Create a log file for links that are not able to connect.
20170426: Add "newline" to csv configuration.
"""

import requests, re, os, sys, csv, datetime
from bs4 import BeautifulSoup


class Downloader():
    def __init__(self):
        self.url='http://www.landchina.com/default.aspx?tabid=263'
        # 2011年后的出让公告
        self.post_data={'TAB_QueryConditionItem':'9f2c3acd-0256-4da2-a659-6949c4671a2a',
                        'TAB_QuerySortItemList':'282:False',
                        # date
                        'TAB_QuerySubmitConditionData':'9f2c3acd-0256-4da2-a659-6949c4671a2a:',  
                        'TAB_QuerySubmitOrderData':'282:False',
                        # page number
                        'TAB_QuerySubmitPagerData':''} 
        self.row_name=[u'行政区', u'电子监管号', u'项目名称', u'项目位置', u'面积(公顷)', u'土地来源',
                      u'土地用途', u'供地方式', u'土地使用年限', u'行业分类', u'土地级别', u'成交价格(万元)',
                      u'土地使用权人', u'约定容积率下限', u'约定容积率上限', u'约定交地时间', u'约定开工时间',
                      u'约定竣工时间', u'实际开工时间', u'实际竣工时间', u'批准单位', u'合同签订日期']
        # 要抓取的数据名称。除了"分期约定"的四项以外全部抓取
        self.information=[
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl',#0
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl',#1
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl',#2
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl',#3
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl',#4
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl',#5
            # 此条为土地来源，抓取为数字，经过换算方得土地来源。
            # 如果‘土地来源’=0 则为’新增建设用地‘
            # 如果’土地来源=‘土地用途’ 则为‘现有建设用地’
            # 如果其他 则为‘新增建设用地（来自存量库）’。
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl',#6  
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl',#7
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl', #8              
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl',#9
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl',#10
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl',#11
##          'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c1_0_ctrl',
##          'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c2_0_ctrl',
##          'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c3_0_ctrl',
##          'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c4_0_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl',#12
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c4_ctrl',                
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c2_ctrl',
            'mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl']

# Step 1
    def date_format(self,year,month,day):
        """
        Import year, month and day, and return date format %Y-%m-%d
        """
        date = datetime.date(year, month, day)
        return date
    
    def days_in_month(self,year,month):
        """
        Calculate how many days in a specific month.
        """
        date = datetime.date(year, month, 1) # The date of the first day of a certain month.
        try:    
            date_next = datetime.date(date.year, date.month + 1, date.day) # The date of the first day of next month.
        except:
            date_next = datetime.date(date.year + 1, 1, date.day)  
        date_distance = (date_next - date).days # How many days in between.
        return date_distance
    
    def get_page_content(self, page_number, date):
        """
        Specify the date to be searched, open the first corresponding page, get the contents.
        """
        post_data = self.post_data.copy()
        # set up the dates to be searched.
        query_date = date.strftime('%Y-%m-%d') + '~' + date.strftime('%Y-%m-%d')
        post_data['TAB_QuerySubmitConditionData'] += query_date
        # set up the page
        post_data['TAB_QuerySubmitPagerData'] = str(page_number)
        try:
        # request the url
            r = requests.post(self.url, data=post_data, timeout=60)
            r.encoding='gb18030'
            page_content = r.text
        except:
            print('Loading page {} timeout!'.format(self.url))
            page_content = u'没有检索到相关数据'
        return page_content

# Step 2
    def get_all_number(self, date):
        """
        Find the number of pages for the date being searched.
        Case 1: no content
        Case 2: only one page of result
        Case 3: 1 to 200 pages
        Case 4: 200 pages above.
        """  
        first_content = self.get_page_content(1, date)
        if u'没有检索到相关数据' in first_content:
            print('Date {} have 0 page.'.format(date))
            return 0
        pattern = re.compile(u'<td.*?class="pager".*?>共(.*?)页.*?</td>')
        result = re.search(pattern, first_content)
        if result == None:
            print('Date {} have 1 page.'.format(date))
            return 1
        if int(result.group(1)) <= 200:
            print('Date {0} have {1} pages.'.format(date, int(result.group(1))))
            return int(result.group(1))
        else:
            print('Date {} seems to be the first ping. Re-try!'.format(date))
            return 200
        
# Step 3
    def get_links(self, page_number, date):
        """get links from a page"""
        page_content = self.get_page_content(page_number, date)
        links = []
        pattern = re.compile(u'<a.*?href="default.aspx.*?tabid=386(.*?)".*?>', re.S)
        results = re.findall(pattern, page_content)
        for result in results:
            links.append('http://www.landchina.com/default.aspx?tabid=386' + result)
        return links
    
    def get_all_links(self, all_number, date):
        """get all links"""
        page_number = 1
        all_links = []
        while page_number <= all_number:
            links = self.get_links(page_number, date)
            all_links += links
            print('Get links from the page {0} out of {1}.'.format(page_number, all_number))
            page_number += 1
        print('Date {0} have {1} links.'.format(date, len(all_links)))
        return all_links
    
# Step 4
    def get_link_content(self, link):
        """
        Open the link to get the content of that link. The content is the report.
        """
        try:
            r=requests.get(link, timeout=60)
            r.encoding='gb18030'
            link_content = r.text
        except:
            print('Loading report from {} timeout!'.format(link))
            link_content = ""
            error_file_name = 'landchina/error.csv'
            if os.path.exists(error_file_name):
                mode = 'a'
            else:
                mode = 'w'
            csv_file = open(error_file_name, mode, newline='', encoding='utf-8-sig')
            writer = csv.writer(csv_file)
            writer.writerow(['{}'.format(link)])
            csv_file.close()
        return link_content
    
    def get_information(self,link_content):
        """
        Get information from every item.
        """
        data = []
        soup = BeautifulSoup(link_content, 'lxml')
        for item in self.information:
            if soup.find(id=item) == None:
                s = ''
            else:
                s = soup.find(id=item).string
                if s == None:
                    s=''                
            data.append(s.strip())
        return data
    
    def save_information(self, data, date):
        """
        Save the information to the file.
        """
#         path is "landchina/year/month/day.csv"
        file_name = 'landchina/{0}/{1}/{2}.csv'.format(datetime.datetime.strftime(date,'%Y'),
                                                      datetime.datetime.strftime(date,'%m'),
                                                      datetime.datetime.strftime(date,'%d'))
        if os.path.exists(file_name):
            mode = 'a'
        else:
            mode = 'w'
        csv_file = open(file_name, mode, newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)
        if mode == 'w':
            writer.writerow([name for name in self.row_name])
        writer.writerow([d for d in data])
        csv_file.close()
        
    def make_directory(self, date):
        """
        Create the directory.
        """
        path = 'landchina/{0}/{1}'.format(datetime.datetime.strftime(date,'%Y'),
                                          datetime.datetime.strftime(date,'%m'))
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            
    def save_all_information(self, all_links, date):
        """
        Save all information from the website.
        """
        for (i,link) in enumerate(all_links):
            link_content = data = None
            link_content = self.get_link_content(link)
            data = self.get_information(link_content)
            self.make_directory(date)
            self.save_information(data, date)
            print('Save information from link {0} out of {1}.'.format(i+1, len(all_links)))
        
    def land_download(self, year, month, day):
        days = self.days_in_month(year, month)
        print('Start downloading!\n')
        # Download month by month
        while day <= days:
            # date
            date = self.date_format(year, month, day)
            # page
            all_number = self.get_all_number(date)
            if all_number == 200:
                all_number = self.get_all_number(date)
            # link
            all_links = self.get_all_links(all_number, date)
            # information
            self.save_all_information(all_links, date)
            day += 1
            print('The information for date {} is all downloaded!\n'.format(date))
        print('The information for month {} is all downloaded!'.format(date.strftime('%Y-%m')))