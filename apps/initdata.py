# -*- encoding: utf-8 -*-
import shioaji as sj
import pandas as pd
import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import threading

class InitStockInfo():
    def __init__(self) -> None:
        pass

    def get_codes_by_market(self, market):
        if market == 'twse':
            url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
        if market == 'tpex':
            url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"
        
        resd = requests.get(url)
        soup = BeautifulSoup(resd.text, 'html.parser')

        table = soup.find_all('table')[1]
        rows = table.find_all('tr')

        # columns 
        first_td = rows[0].find_all('td')
        columns = [tr.text.strip() for tr in first_td if tr.text.strip()]
        colnames = columns[0:6]

        # content
        content = []
        for tr in rows:
            td = tr.find_all('td')
            row = [tr.text.strip() for tr in td if tr.text.strip()]
            if len(row) == 6:
                content.append(row)

        # convert to df
        df = pd.DataFrame(content, columns=colnames)
        df['有價證券代號及名稱'] = df['有價證券代號及名稱'].apply(lambda x:x.split('\u3000'))
        df['代號'] = df['有價證券代號及名稱'].apply(lambda x:x[0])
        df['name'] = df['有價證券代號及名稱'].apply(lambda x:x[1])
        df['codelimit'] = df['代號'].apply(lambda x:len(x)==4)
        res = df[df['codelimit']].copy()
        res['code'] = res['代號']
      
        return res[['code','name']]

    def get_all_codes(self):   
        print('start')
        twse_codes = self.get_codes_by_market('twse')
        tpex_codes = self.get_codes_by_market('tpex')  
        print('finish')
        return twse_codes.append(tpex_codes)

    def get_marketvalue_list(self):
        url = 'https://stock.capital.com.tw/z/zm/zmd/zmdb.djhtm'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find_all('table')[0]

        table.find_all("a", href=re.compile("javascript:Link2Stk"))
        ranks = [i.text[0:4] for i in table.find_all("a", href=re.compile("javascript:Link2Stk"))]
        return ranks[0:20]  

    def get_code_categorys(self):
        categorylist = [
            {'code': '1101', 'name': '台泥', 'category': '傳產-水泥'} ,
            {'code': '1102', 'name': '亞泥', 'category': '傳產-水泥'} ,
            {'code': '1110', 'name': '東泥', 'category': '傳產-水泥'} ,
            {'code': '1103', 'name': '嘉泥', 'category': '傳產-水泥'} ,
            {'code': '1109', 'name': '信大', 'category': '傳產-水泥'} ,
            {'code': '1104', 'name': '環泥', 'category': '傳產-水泥'} ,
            {'code': '1108', 'name': '幸福', 'category': '傳產-水泥'} ,
            {'code': '1229', 'name': '聯華', 'category': '傳產-食品'} ,
            {'code': '1210', 'name': '大成', 'category': '傳產-食品'} ,
            {'code': '1216', 'name': '統一', 'category': '傳產-食品'} ,
            {'code': '1215', 'name': '卜蜂', 'category': '傳產-食品'} ,
            {'code': '1201', 'name': '味全', 'category': '傳產-食品'} ,
            {'code': '1227', 'name': '佳格', 'category': '傳產-食品'} ,
            {'code': '6026', 'name': '福邦證', 'category': '金融-證券'} ,
            {'code': '6005', 'name': '群益證', 'category': '金融-證券'} ,
            {'code': '6015', 'name': '宏遠證', 'category': '金融-證券'} ,
            {'code': '2855', 'name': '統一證', 'category': '金融-證券'} ,
            {'code': '6016', 'name': '康和證', 'category': '金融-證券'} ,
            {'code': '6024', 'name': '群益期', 'category': '金融-證券'} ,
            {'code': '6023', 'name': '元大期', 'category': '金融-證券'} ,
            {'code': '5864', 'name': '致和證', 'category': '金融-證券'} ,
            {'code': '6021', 'name': '大慶證', 'category': '金融-證券'} ,
            {'code': '6020', 'name': '大展證', 'category': '金融-證券'} ,
            {'code': '2883', 'name': '開發金', 'category': '金融-金控'} ,
            {'code': '2881', 'name': '富邦金', 'category': '金融-金控'} ,
            {'code': '2887', 'name': '台新金', 'category': '金融-金控'} ,
            {'code': '2882', 'name': '國泰金', 'category': '金融-金控'} ,
            {'code': '2888', 'name': '新光金', 'category': '金融-金控'} ,
            {'code': '2884', 'name': '玉山金', 'category': '金融-金控'} ,
            {'code': '2880', 'name': '華南金', 'category': '金融-金控'} ,
            {'code': '2890', 'name': '永豐金', 'category': '金融-金控'} ,
            {'code': '2891', 'name': '中信金', 'category': '金融-金控'} ,
            {'code': '2886', 'name': '兆豐金', 'category': '金融-金控'} ,
            {'code': '2885', 'name': '元大金', 'category': '金融-金控'} ,
            {'code': '5880', 'name': '合庫金', 'category': '金融-金控'} ,
            {'code': '2889', 'name': '國票金', 'category': '金融-金控'} ,
            {'code': '2892', 'name': '第一金', 'category': '金融-金控'} ,
            {'code': '5820', 'name': '日盛金', 'category': '金融-金控'}
        ]
        return pd.DataFrame(categorylist)
    
    def main(self):
        global allcodes, code_categorys, mvlist
        allcodes = self.get_all_codes()
        code_categorys = self.get_code_categorys()
        mvlist = self.get_marketvalue_list()


class GetContracts():
    def __init__(self) -> None:
        pass

    def get_overviews(self):
        contracts = [sjapi.Contracts.Stocks[ticker] for ticker in allcodes.code]
        snapshots = sjapi.snapshots(contracts)
        df_stocks = pd.DataFrame(snapshots)

        tse_groups = list(sjapi.Contracts.Indexs["TSE"])[1:37]
        groups_names = {i.symbol: i.name for i in tse_groups}
        contracts= tse_groups
        snapshots = sjapi.snapshots(contracts)
        df_groups = pd.DataFrame(snapshots)
        df_groups['group_index'] = df_groups['code'].apply(lambda x:groups_names['TSE'+x])
        df_groups = df_groups[['change_type','change_rate','total_amount','group_index','volume_ratio']]
        return df_stocks, df_groups

    def get_change_counts(self, df):
        counts = df.change_type.value_counts().to_dict()
        return str(counts["LimitUp"])+' / '+str(counts["Up"])+' / '+ str(counts["Down"]) +' / '+  str(counts["LimitDown"]) + ' / '+  str(counts["Unchanged"])

    def get_exchange_overviews(self):
        contracts = [sjapi.Contracts.Futures.TXF.TXFR1, sjapi.Contracts.Indexs["TSE"]["TSE001"], sjapi.Contracts.Indexs["OTC"]["OTC101"]]
        snapshots = sjapi.snapshots(contracts)
        df = pd.DataFrame(snapshots)
        df = df[['exchange','high', 'low', 'open', 'close', 'change_rate','volume_ratio']]

        df['high_low_diff'] = df['high'] - df['low']
        exchange_diff = round(df[df.exchange == 'TAIFEX'].close.values[0] - df[df.exchange == 'TSE'].close.values[0],2)
        res = df[['exchange','close','open','high','low','high_low_diff','change_rate','volume_ratio']]
        return exchange_diff,  res.to_dict('records')


    def get_filtered_stocks(self, stocks):
        df = stocks.copy()
        df['change_info'] = df['change_type'] +','+df['change_rate'].apply(str)
        df['bias'] = (df.close - df.average_price)/df.average_price
        dff = df[['code','exchange','close','change_info','volume_ratio','change_rate','bias','total_amount']].copy()
        tmp = pd.merge(dff, code_categorys, how="left", on=["code"])
        tmp['momentum'] = round(tmp.change_rate * tmp.volume_ratio, 2)
        long_stocks = tmp[(tmp.momentum > 1)].sort_values('momentum', ascending=False).head(20)
        short_stocks = tmp[(tmp.momentum < -1)].sort_values('momentum', ascending=True).head(20)
        return long_stocks.to_dict('records'), short_stocks.to_dict('records')

    def clean_amount_rank(self, stocks):
        df = stocks.copy()
        df['change_info'] = df['change_type'] +','+df['change_rate'].apply(str)
        dff = df[['code','exchange','close','change_info','change_rate','volume_ratio','total_amount']].copy()
        mer = pd.merge(dff, code_categorys, how="left", on=["code"])
        return mer.to_dict('records')

    def clean_marketvalue_top(self, stocks):
        df = stocks.set_index('code').loc[mvlist].reset_index().copy()
        df['change_info'] = df['change_type'] +','+df['change_rate'].apply(str)
        dff = df[['code','exchange','close','change_info','change_rate','volume_ratio','total_amount']].copy()
        mer = pd.merge(dff, code_categorys, how="left", on=["code"])
        return mer.to_dict('records')

    def get_filtered_groups(self, groups):
        df = groups.copy()
        total_amount_sum = df.total_amount.sum()
        
        df['amount_ratio'] = df['total_amount'].apply(lambda x:(round(x/total_amount_sum,2))*100)
        df['momentum'] = df.change_rate * df.volume_ratio
        df = df.sort_values('momentum',ascending=False)
        long_groups = df[df.momentum > 0].head(6)
        short_groups = df[df.momentum < 0].sort_values('momentum',ascending=True).head(6)
        
        return long_groups[['group_index','change_rate','volume_ratio','amount_ratio']].to_dict('records'), short_groups[['group_index','change_rate','volume_ratio','amount_ratio']].to_dict('records')
        
      

# 執行子執行緒
login_api = LoginAPI()
print('.... login api ....')
threading.Thread(target=login_api.login()).start()

init_stockinfo = InitStockInfo()
print('.... init stockinfo ....')
threading.Thread(target=init_stockinfo.main()).start()

