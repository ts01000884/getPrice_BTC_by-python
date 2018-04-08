# coding=UTF-8
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os, urllib, urllib2
from urllib2 import urlopen, Request
from time import strftime
import time
import re
import pymysql
pymysql.install_as_MySQLdb()



def getPrice(text1):                        #處理價格字串
    ans=""
    temp=""
    temp=text1
    
    temp1=temp.split("span")
    print temp1

    return ans 



reload(sys)
sys.setdefaultencoding('utf8')

# 開啟網頁



browser_bitoex = webdriver.Firefox()
browser_bitoex.get("https://www.bitoex.com/charts?locale=zh-tw")
time.sleep(5) 
data_bitoex = browser_bitoex.page_source                                  #擷取網站原始碼
soup_bitoex = BeautifulSoup(data_bitoex, "html.parser")                   #使用BS進行分析
browser_bitoex.quit();                                            #關閉瀏覽器
div_buy = soup_bitoex.find('h4', {'class': 'sync_rate_buy'})
div_sell = soup_bitoex.find('h4', {'class': 'sync_rate_sell'})


kkk=""
for tag in div_buy:
    kkk=tag.string
buyprice=''.join([x for x in kkk if x.isdigit()])                   #過濾標點符號

for tag in div_sell:
    kkk=tag.string
sellprice=''.join([x for x in kkk if x.isdigit()])


print buyprice
print sellprice


browser_twdusd = webdriver.Firefox()                                #抓台幣匯率
browser_twdusd.get("http://rate.bot.com.tw/xrt?Lang=zh-TW")
time.sleep(5)
data_twdusd = browser_twdusd.page_source                                  #擷取網站原始碼
soup_twdusd = BeautifulSoup(data_twdusd, "html.parser")                   #使用BS進行分析
browser_twdusd.quit();                                            #關閉瀏覽器
div_twd = soup_twdusd.find('td', {'class': 'rate-content-cash text-right print_hide'})


for tag in div_twd:
    kkk=tag.string
    break

twdusd=kkk                                      #台灣銀行掛牌匯率
print kkk

browser_btc = webdriver.Firefox()                                #抓彼特必金額
browser_btc.get("https://blockchain.info/")
time.sleep(5)
data_btc = browser_btc.page_source                                  #擷取網站原始碼
data_btc = BeautifulSoup(data_btc, "html.parser")                   #使用BS進行分析
browser_btc.quit();                                            #關閉瀏覽器
div_btc = data_btc.find('span', {'class': 'exchange-rate'})


for tag in div_btc:
    kkk=tag.string
    break
btcprice=kkk.replace(',','')            #彼特必價格

ret=[btcprice,buyprice,sellprice,twdusd]
sql="INSERT INTO BTC_BTIOEX (btc_price_usd, btc_buyprice_twd, btc_sellprice_twd,usd_twd) VALUES ("+btcprice+","+buyprice+","+sellprice+","+twdusd+");"
db = pymysql.connect(host="127.0.0.1",
    user="homestead", passwd="secret", db="homestead",port=33060)
cursor = db.cursor()
cursor.execute(sql)
db.commit()

db.close()


#print div_lotstars



