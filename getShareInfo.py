from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import datetime
import time

stock_list_df = pd.read_csv("stock_list.csv")

portfolio_columns = [
"code",
"name",
"sector",
"shares",
"stock price",
"asset per company",
"dividend yield",
"PER",
"PBR",
"sales",
"operationg income",
"operationg margin",
"current ratio",
"dividend",
"payout ratio"
]

# stock_price_column = [
# "stock price"
# ]
#
# financial_statements_list = [
# "Sales/last year",
# "operationg income",
# "operationg margin",
# "current ratio",
# "dividend"
# ]

stock_price_index = 0
dividend_index = 32
PER_index = 41
PBR_index = 51
dividend_yield_index = 60
current_ratio_index =63
payout_ratio_index=66
operationg_margin_index = 82
sales_index = 129
operationg_income_index = 133

index_num = [
stock_price_index,
dividend_index,
PER_index,
PBR_index,
dividend_yield_index,
current_ratio_index,
payout_ratio_index,
operationg_margin_index,
sales_index,
operationg_income_index
]

class_name = "TextLabel__text-label___3oCVw TextLabel__black___2FN-Z TextLabel__regular___2X0ym digits MarketsTable-value-FP5ul"


result = []
for i in range(len(stock_list_df)):
    url="https://jp.reuters.com/companies/{0}.T/key-metrics" .format(stock_list_df.iloc[i,1])
    r = requests.get(url)
    time.sleep(0.5)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.title.text)
    company_all_info = soup.find_all("span",{"class":{class_name}})
    stock_price = ""
    company_info = []
    try:
        if company_all_info[stock_price_index].get_text().find(",")== -1:
            stock_price = company_all_info[stock_price_index].get_text()
        else:
            stock_price = company_all_info[stock_price_index].get_text().replace(",","")
        print(stock_list_df.iloc[i,6],stock_price)
        company_info = [
        stock_list_df.iloc[i,1],#code
        stock_list_df.iloc[i,2],#name
        stock_list_df.iloc[i,4],#sector
        stock_list_df.iloc[i,6],#stock
        company_all_info[stock_price_index].get_text(),
        int(stock_list_df.iloc[i,6])*float(stock_price),
        company_all_info[dividend_yield_index].get_text(),
        company_all_info[PER_index].get_text(),
        company_all_info[PBR_index].get_text(),
        company_all_info[sales_index].get_text(),
        company_all_info[operationg_income_index].get_text(),
        company_all_info[operationg_margin_index].get_text(),
        company_all_info[current_ratio_index].get_text(),
        company_all_info[dividend_index].get_text(),
        company_all_info[payout_ratio_index].get_text()
        ]

        result.append(company_info)
    except IndexError:
        pass

portfolio_df = pd.DataFrame(result, columns=portfolio_columns)

date_info = datetime.date.today().strftime("%Y%m%d")
portfolio_df.to_csv("{0}_portfolio.csv".format(date_info))

print("Well Done!!")
