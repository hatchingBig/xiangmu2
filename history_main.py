# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:51:22 2018

@author: Administrator
"""


import urllib
import re
import time as tag
import pandas as pd
from dateutil.parser import parse
import os
import datetime
from GetHistoryList import get_history_stock_list

def parse_data(urlid,thetype):
    if thetype == 'stock':
        try:
            stock_url = 'http://quotes.money.163.com/trade/lsjysj_{}.html'.format(urlid)
            ff = urllib.request.urlopen(stock_url)
            isnormal = True
        except:
            isnormal = False
        if isnormal:
            d = ff.read().decode('utf8')
            start_p = d.index('<select name="year">')
            stop_p = d.index('<select name="season">')
            content = d[start_p+20:stop_p]
            least_year = int(content.split('<option value="')[-1][:4])
            year_list = list(range(least_year,2019))
            season_list = [1,2,3,4]
            cach_total = []
            for year in year_list:
                for season in season_list:
                    tag.sleep(1)
                    sub_url = 'http://quotes.money.163.com/trade/lsjysj_{}.html?year={}&season={}'.format(urlid,year,season)
                    sub_ff = urllib.request.urlopen(sub_url)
                    sub_d = sub_ff.read().decode('utf8')
                    sub_start_p = sub_d.index('<table class="table_bg001 border_box limit_sale">')
                    sub_stop_p = sub_d.index('<div id="dropBox1" class="drop_box">')
                    sub_content = sub_d[sub_start_p:sub_stop_p]
                    pattern = re.compile(u"<th>(.*?)</th>")
                    columns_list = pattern.findall(sub_content)
                    df = pd.DataFrame(columns = columns_list)
                    try:
                        sub_second_start_p = sub_content.index('<tr class=\'\'>')
                        real_content = sub_content[sub_second_start_p:]
                        real_content_list = re.sub(u"\\<.*?\\>", "cqd", real_content).split('cqd')
                        cach_content = []
                        for i in real_content_list:
                            i = i.replace(' ','')
                            if i!='' and i!='\r\n':
                                cach_content.append(i)
                        assert len(cach_content) // len(columns_list) == len(cach_content) / len(columns_list)
                        for i in range(len(cach_content)//len(columns_list)):
                            df.loc[i] = cach_content[len(columns_list)*i:(i+1)*len(columns_list)]
                        cach_total.append(df)
                    except:
                        pass
            final_df = pd.concat(cach_total)
            final_df['parse'] = final_df['日期'].map(lambda x:parse(x))
            final_df = final_df.sort_values(by='parse')
            final_df = final_df.drop('parse',axis=1)
        else:
            final_df = pd.DataFrame()
        return final_df
    elif thetype == 'zhishu':
        try:
            etf_url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_{}.html'.format(urlid) 
            ff = urllib.request.urlopen(etf_url)
            isnormal = True
        except:
            isnormal = False
        if isnormal:
            d = ff.read().decode('utf8')
            start_p = d.index('<select name="year">')
            stop_p = d.index('<select name="season">')
            content = d[start_p+20:stop_p]
            least_year = int(content.split('<option value="')[-1][:4])
            year_list = list(range(least_year,2019))
            season_list = [1,2,3,4]
            cach_total = []
            for year in year_list:
                for season in season_list:
                    tag.sleep(1)
                    sub_url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_{}.html?year={}&season={}'.format(urlid,year,season)
                    sub_ff = urllib.request.urlopen(sub_url)
                    sub_d = sub_ff.read().decode('utf8')
                    sub_start_p = sub_d.index('<table class="table_bg001 border_box limit_sale">')
                    sub_stop_p = sub_d.index('<div id="dropBox1" class="drop_box">')
                    sub_content = sub_d[sub_start_p:sub_stop_p]
                    pattern = re.compile(u"<th>(.*?)</th>")
                    columns_list = pattern.findall(sub_content)
                    df = pd.DataFrame(columns = columns_list)
                    try:
                        sub_second_start_p = sub_content.index('<tr class=\'\'>')
                        real_content = sub_content[sub_second_start_p:]
                        real_content_list = re.sub(u"\\<.*?\\>", "cqd", real_content).split('cqd')
                        cach_content = []
                        for i in real_content_list:
                            i = i.replace(' ','')
                            if i!='' and i!='\r\n':
                                cach_content.append(i)
                        assert len(cach_content) // len(columns_list) == len(cach_content) / len(columns_list)
                        for i in range(len(cach_content)//len(columns_list)):
                            df.loc[i] = cach_content[len(columns_list)*i:(i+1)*len(columns_list)]
                        cach_total.append(df)
                    except:
                        pass
            final_df = pd.concat(cach_total)
            final_df['parse'] = final_df['日期'].map(lambda x:parse(x))
            final_df = final_df.sort_values(by='parse')
            final_df = final_df.drop('parse',axis=1)
        else:
            final_df = pd.DataFrame()
        return final_df
    elif thetype == 'etf':
        today = str(datetime.datetime.now())[:10]
        isfunc = True
        count_func = 0
        cach_big = []
        while isfunc:
            try:
                etf_url = 'http://quotes.money.163.com/fund/jzzs_{}_{}.html?start=2008-01-01&end={}&sort=TDATE&order=desc'.format(urlid,count_func,today) 
                ff = urllib.request.urlopen(etf_url)
                d = ff.read().decode('utf8')
                start_p = d.index('<div class="fn_fund_tb_content" id="fn_fund_value_trend">')
                stop_p = d.index('<div class="mod_pages">')
                content = d[start_p:stop_p]
                real_content = re.sub(u"\\<.*?\\>", "cqd", content).split('cqd')
                cach_etf= []
                for item in real_content:
                    item = item.replace('\r','')
                    item = item.replace('\n','')
                    item = item.replace(' ','')
                    if item!='':
                        cach_etf.append(item)
                assert len(cach_etf) // 4 == len(cach_etf) / 4
                if len(cach_etf) == 4:
                    isfunc = False
                    continue
                columns_list = cach_etf[:4]
                content_list = cach_etf[4:]
                df = pd.DataFrame(columns = columns_list)
                for i in range(len(content_list) // 4):
                    df.loc[i] = content_list[4*i:(i+1)*4]
                cach_big.append(df)
                count_func += 1
            except:
                isfunc = False
        if len(cach_big) != 0:
            final_df = pd.concat(cach_big)
            final_df['parse'] = final_df['公布日期'].map(lambda x:parse(x))
            final_df = final_df.sort_values(by='parse')
            final_df = final_df.drop('parse',axis=1)
        else:
            final_df = pd.DataFrame()
        return final_df

def main():
    small_sleep = 0.3
    big_sleep = 10
    bad_case_thershold = 2
    tlist = get_history_stock_list()
    for item in tlist:
        if len(item)>6:
            item_new = item.replace('.html','')
            this_stock = item_new.split('/')[-1][2:]
        else:
            this_stock = item
        flag = os.path.exists('etf\{}.csv'.format(this_stock)) or \
                os.path.exists('stock\{}.csv'.format(this_stock)) or \
                os.path.exists('zhishu\{}.csv'.format(this_stock))
        tag.sleep(small_sleep)
        isonetf = isonstock = isonzhishu = False
        if not flag:
            isetf = True
            isstock = True
            iszhishu = True
            count_zhishu = 0
            while iszhishu:
                df_zhishu = pd.DataFrame()
                try:
                    df_zhishu = parse_data(this_stock,'zhishu')
                    iszhishu = False
                except:
                    tag.sleep(big_sleep)
                    count_zhishu += 1
                    print('{}zhishu正在延迟'.format(this_stock))
                if count_zhishu == bad_case_thershold:
                    iszhishu = False
                    with open('log.txt','a') as zhishuf:
                        zhishuf.write('{}_zhishu_failed!\n'.format(this_stock))
                        zhishuf.close()                    
            if df_zhishu.shape[0]>5 and count_zhishu != bad_case_thershold:
                df_zhishu.to_csv('zhishu\{}.csv'.format(this_stock),index=False)
                isonzhishu = True
            count_stock = 0
            while isstock:
                df_stock = pd.DataFrame()
                try:
                    df_stock = parse_data(this_stock,'stock')
                    isstock = False
                except:
                    tag.sleep(big_sleep)
                    count_stock += 1
                    print('{}stock正在延迟'.format(this_stock))
                if count_stock == bad_case_thershold:
                    isstock = False
                    with open('log.txt','a') as stockf:
                        stockf.write('{}_stock_failed!\n'.format(this_stock))
                        stockf.close()                     
            if df_stock.shape[0]>5 and count_stock != bad_case_thershold:
                df_stock.to_csv('stock\{}.csv'.format(this_stock),index=False)
                isonstock = True
            count_etf = 0
            while isetf:
                df_etf = pd.DataFrame()
                try:
                    df_etf = parse_data(this_stock,'etf')
                    isetf = False
                except:
                    tag.sleep(big_sleep)
                    count_etf += 1
                    print('{}etf正在延迟'.format(this_stock))
                if count_etf == bad_case_thershold:
                    isetf = False
                    with open('log.txt','a') as etff:
                        etff.write('{}_etf_failed!\n'.format(this_stock))
                        etff.close()                    
            if df_etf.shape[0]>5 and count_etf != bad_case_thershold:
                df_etf.to_csv('etf\{}.csv'.format(this_stock),index=False)
                isonetf = True                
            if (isonetf == isonstock == isonzhishu == False):
                print('{}_数据不存在'.format(this_stock))
            else:
                print('{}_配置完毕'.format(this_stock))
main()
                    