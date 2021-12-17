import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
pd.set_option('display.float_format', lambda x: '%.5f' % x)
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (12, 8)

st.sidebar.title("Finance App")
st.sidebar.write("All of the calculations are based on data from the MSE index website where official financial reports of the companies are uploaded usually on a quarterly basis.")
menu_selection = ["APU", "SUU"]
company = st.sidebar.selectbox("Companies in Classification 1", menu_selection)
st.sidebar.write("This app is created for school purposes only.")

### APU
if company == "APU":
    st.title("APU LC")
    st.write("Since its establishment, APU has been writing the history of beverages in Mongolia and always leading through its policy, activities, development, achievement and success over the past 90 years.")

    col1, col2 = st.columns([1,1])

    with col1:
        apu_stock_df = pd.read_csv("apuStock.csv", thousands=",")
        min_date = st.date_input("The first date")
        min_date = pd.to_datetime(min_date)

    with col2:
        max_date = st.date_input("The second date")
        max_date = pd.to_datetime(max_date)

    apu_stock_df = pd.read_csv("apuStock.csv", thousands=",")
    apu_stock_df['date'] = pd.to_datetime(apu_stock_df['date'])
    apu_stock_df = apu_stock_df[(apu_stock_df['date'] >= min_date) & (apu_stock_df['date'] <= max_date)]
    fig = px.line(apu_stock_df, x="date", y="value", title="APU's Stock price overtime", labels={"date": "Date", "value": "Stock price"})
    st.plotly_chart(fig)

    with st.expander("Forecast"):
        sheet_selection = ["Balance Sheet", "Income Statement"]
        sheet = st.selectbox("Choose the financial sheet", sheet_selection)

        if sheet == "Balance Sheet":
            st.subheader("Balance Sheet - Forecast")
            if st.button('See as a table'):
                apu_forecast = pd.read_csv("APU Forecast.csv", thousands=",")
                st.dataframe(apu_forecast)
            apu_forecast = pd.read_csv("APU Forecast.csv", thousands=",")

            tae = apu_forecast[(apu_forecast['Breakdown'] == "Total Liability") | (apu_forecast['Breakdown'] == "Total Equity")].reset_index().drop(columns="index", axis=1)
            tae = pd.DataFrame.transpose(tae).reset_index()
            tae.columns = tae.iloc[0]
            tae = tae.drop([0], axis=0)
            tae['Breakdown'] = tae['Breakdown'].str[0:4].astype(int)
            fig = px.line(tae, x='Breakdown', y=['Total Liability', 'Total Equity'], title="Total Liability vs Total Equity Forecast (2021-2025)", labels={"Breakdown": "Year", "value": "In thousand tugriks"})
            fig.add_shape(type="line", x0=2021, y0=0, x1=2021, y1=600000000,line=dict(color="MediumPurple",width=3,dash="dot",))
            st.plotly_chart(fig)

            ca = apu_forecast[1:5]
            ca['Average'] = (ca['2015']+ca['2016']+ca['2017']+ca['2018']+ca['2019']+ca['2020']+ca['2021F']+ca['2022F']+ca['2023F']+ca['2024F']+ca['2025F'])/11
            fig = px.bar(ca, x='Breakdown', y='Average', title="Average current asset breakdown")
            st.plotly_chart(fig)

        if sheet == "Income Statement":
            st.subheader("Income Statement - Forecast")
            if st.button('See as a table'):
                apu_forecast_ins = pd.read_csv("APU Forecast ins.csv", thousands=",")
                st.dataframe(apu_forecast_ins)

            apu_forecast_ins = pd.read_csv("APU Forecast ins.csv", thousands=",")
            income = apu_forecast_ins[(apu_forecast_ins['Breakdown'] == "Gross Profit") | (apu_forecast_ins['Breakdown'] == "Net Income")].reset_index().drop(columns="index", axis=1)
            income = pd.DataFrame.transpose(income).reset_index()
            income.columns = income.iloc[0]
            income = income.drop([0], axis=0)
            income['Breakdown'] = income['Breakdown'].str[0:4].astype(int)
            fig = px.line(income, x='Breakdown', y=['Gross Profit', 'Net Income'], title="Gross and Net income over time (2021-2025)", labels={"Breakdown": "Year", "value": "In thousand tugriks"})
            fig.add_shape(type="line", x0=2021, y0=0, x1=2021, y1=250000000,line=dict(color="MediumPurple",width=3,dash="dot",))
            st.plotly_chart(fig)

            in_ex = apu_forecast_ins[(apu_forecast_ins['Breakdown'] == "Operating Income") | (apu_forecast_ins['Breakdown'] == "Operating Expense")].reset_index().drop(columns="index", axis=1)
            in_ex = pd.DataFrame.transpose(in_ex).reset_index()
            in_ex.columns = in_ex.iloc[0]
            in_ex = in_ex.drop([0], axis=0)
            in_ex['Breakdown'] = in_ex['Breakdown'].str[0:4].astype(int)
            fig = px.line(in_ex, x='Breakdown', y=['Operating Income', 'Operating Expense'], title="Operating Income vs Expense (2021-2025)", labels={"Breakdown": "Year", "value": "In thousand tugriks"})
            fig.add_shape(type="line", x0=2021, y0=0, x1=2021, y1=170000000,line=dict(color="MediumPurple",width=3,dash="dot",))
            st.plotly_chart(fig)

    with st.expander("Ratio Analysis"):
        st.write("All of the calculations are based on data from the MSE index website where official financial reports of the companies are uploaded usually on a quarterly basis. The MSE A index or otherwise the best performing 20 companies out of all other organizations in Mongolia, industry average will be taken whilst excluding companies that are service oriented. The ratios of the company will be assessed based on the industry averages and overall average.")
        
        ratio_selection = ["Activity Ratios", "Liquidity Ratios", "Leverage Ratios", "Profitability Ratios", "Valuation Ratios"]
        ratio = st.selectbox("Choose the ratio type", ratio_selection)

        apu_forecast_ins = pd.read_csv("APU Forecast ins.csv", thousands=",")
        apu_forecast = pd.read_csv("APU Forecast.csv", thousands=",")
        mse_index = pd.read_csv("mse index.csv", thousands=",")
        mse_index = mse_index[['Ratio Names', 'MSE A Index']].dropna()

        balance_ratio = apu_forecast[['Breakdown', '2020']].dropna()
        state_ratio = apu_forecast_ins[['Breakdown', '2020']].dropna()

        if ratio == "Activity Ratios":
            st.header("Activity Ratios")
            st.write("Activity ratios measure how efficiently a company performs day-to-day tasks, such as the collection of receivables and management of inventory.")

            st.subheader("Days of Inventory on hand (DOH)")
            doh = 365/((state_ratio[state_ratio['Breakdown'] == "COGS"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Inventory"]['2020'].values))
            doh = doh[0]
            mse = mse_index[mse_index['Ratio Names'] == "Days of inventory on hands (DOH)"]['MSE A Index'][0]
            if doh > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [doh], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Days of inventory on the hands (DOH) ratio is smaller than the MSE Index which means that the company is using its inventory more efficiently and frequently, which can result in potentially higher profit.")

            st.subheader("Days of Sales outstanding (DSO)")
            dso = 365/((state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Accounts Receivable"]['2020'].values))
            dso = dso[0]
            mse = mse_index[mse_index['Ratio Names'] == "Days of Sales outstanding (DSO)"]['MSE A Index'][1]
            if dso > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [dso], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("In 2019, APU was doing almost the same as the MSE Index. In one year, they increased their receivables turnover by 2.5 which indicates that customers are paying on time and the company is doing a good job collecting its receivables. By doing so, they are collecting their debts in a shorter amount of time which makes their Days of sales outstanding (DSO) ratio relatively lower than the industry average. So the company is handling their cash flow ideally.")

            st.subheader("Number of days of Payables")
            apd = 365/((state_ratio[state_ratio['Breakdown'] == "COGS"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Accounts Payable"]['2020'].values))
            apd = apd[0]
            mse = mse_index[mse_index['Ratio Names'] == "Number of days of payables"]['MSE A Index'][2]
            if apd > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [apd], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Their payable turnover is much higher than the industry showing that they quickly pay their debts which makes them more desirable for lenders. According to the index, in average it takes 78 days for Class 1 companies to pay their suppliers while APU takes 8 days.")

            st.subheader("Fixed Asset Turnover")
            fat = (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Fixed Asset"]['2020'].values)
            fat = fat[0]
            mse = mse_index[mse_index['Ratio Names'] == "Fixed asset turnover"]['MSE A Index'][3]
            if fat > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [fat], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("APU should pay more attention to managing their fixed assets efficiently.  Their fixed asset turnover is 4 times less than the average of their peers.")

            st.subheader("Total Asset Turnover")
            tat = (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Asset"]['2020'].values)
            tat = tat[0]
            mse = mse_index[mse_index['Ratio Names'] == "Total asset turnover"]['MSE A Index'][4]
            if tat > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [tat], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("APU is generating slightly higher revenue per tugrik of assets than the index. ")

        if ratio == "Liquidity Ratios":
            st.header("Liquidity Ratios")
            st.write("Liquidity ratios measure the company’s ability to meet its short-term obligations and how quickly assets are converted into cash.")

            st.subheader("Current Ratio")
            cr = (balance_ratio[balance_ratio['Breakdown'] == "Current Asset"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Current Liability"]['2020'].values)
            cr = cr[0]
            mse = mse_index[mse_index['Ratio Names'] == "Current"]['MSE A Index'][5]
            if cr > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [cr], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("In 2019, the current ratio of APU was relatively higher than the industry average and the number decreased in 2020 which could indicate that they started investing their current assets for better returns. There is a low risk of distress or default.")

            st.subheader("Quick Ratio")
            qr = ((balance_ratio[balance_ratio['Breakdown'] == "Current Asset"]['2020'].values) - (balance_ratio[balance_ratio['Breakdown'] == "Inventory"]['2020'].values)) / (balance_ratio[balance_ratio['Breakdown'] == "Current Liability"]['2020'].values)
            qr = qr[0]
            mse = mse_index[mse_index['Ratio Names'] == "Quick"]['MSE A Index'][6]
            if qr > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [qr], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Lower quick ratio means they don’t struggle with paying their debts. They are capable of paying all their liabilities by their inventory excluding current assets.")

            st.subheader("Cash Conversion Cycle")
            doh = (365/((state_ratio[state_ratio['Breakdown'] == "COGS"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Inventory"]['2020'].values)))[0]
            dso = (365/((state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Accounts Receivable"]['2020'].values)))[0]
            apd = (365/((state_ratio[state_ratio['Breakdown'] == "COGS"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Accounts Payable"]['2020'].values)))[0]

            ccc = doh + dso - apd
            mse = mse_index[mse_index['Ratio Names'] == "Cash conversion cycle"]['MSE A Index'][7]
            if ccc > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [ccc], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Cash conversion cycle represents how fast a company can convert the invested cash from start (investment) to end (returns). A lower cash conversion cycle indicates that a company has a fast inventory-to-sales pipeline.")

        if ratio == "Leverage Ratios":
            st.header("Leverage Ratios")
            st.write("Leverage ratios or solvency ratios measure a company’s ability to meet long-term obligations. Subsets of these ratios are also known as “leverage” and “long-term debt” ratios")

            st.subheader("Debt to asset")
            dta =(balance_ratio[balance_ratio['Breakdown'] == "Short-term Debt"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Long-term Liability"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Asset"]['2020'].values)
            dta = dta[0]
            mse = mse_index[mse_index['Ratio Names'] == "Debt to asset"]['MSE A Index'][8]
            if dta > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [dta], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("The company is relatively safe from default risk with the debt to asset ratio of 0.0511. The small portion of assets is funded with debt.")

            st.subheader("Debt to capital")
            dtc =(balance_ratio[balance_ratio['Breakdown'] == "Short-term Debt"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Long-term Liability"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Short-term Debt"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Long-term Liability"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values)
            dtc = dtc[0]
            mse = mse_index[mse_index['Ratio Names'] == "Debt to capital"]['MSE A Index'][9]
            if dtc > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [dtc], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Based on the debt to capital ratio, APU is a much more suitable and less risky investment for investors. Their debt to capital ratio is less than the industry average meaning they have a better financial structure.")

            st.subheader("Debt to equity")
            dte =(balance_ratio[balance_ratio['Breakdown'] == "Short-term Debt"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Long-term Liability"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values)
            dte = dte[0]
            mse = mse_index[mse_index['Ratio Names'] == "Debt to equity"]['MSE A Index'][10]
            if dte > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [dte], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("The debt-to-equity (D/E) ratio compares a company's total liabilities to its shareholder equity and can be used to evaluate how much leverage a company is using. APU company itself or it's stock has much lower risk to shareholders.")

            st.subheader("Financial Leverage")
            fl = balance_ratio[balance_ratio['Breakdown'] == "Total Asset"]['2020'].values / balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values
            fl = fl[0]
            mse = mse_index[mse_index['Ratio Names'] == "Financial leverage"]['MSE A Index'][11]
            if fl > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [fl], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Slightly higher than the MSE index average financial leverage ratio indicates that they are capable of paying off their liabilities better than their peers which could attract more creditors. But decreased cash ratio might be indicating that they might face financial difficulties in the near future.")        

        if ratio == "Profitability Ratios":
            st.header("Profitability Ratios")
            st.write("Profitability ratios measure the company’s ability to generate profits from its resources (assets).")

            st.subheader("Gross Profit Margin")
            gpm =(state_ratio[state_ratio['Breakdown'] == "Gross Profit"]['2020'].values) / (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values)
            gpm = gpm[0]
            mse = mse_index[mse_index['Ratio Names'] == "Gross profit margin"]['MSE A Index'][12]
            if gpm > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [gpm], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("It shows that 47.7% of sales revenue APU keeps after it covers all direct costs associated with running the business. And it is almost two times higher than the average of Classification 1 companies.")

            st.subheader("Pretax Margin")
            ptm =(state_ratio[state_ratio['Breakdown'] == "EBT"]['2020'].values) / (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values)
            ptm = ptm[0]
            mse = mse_index[mse_index['Ratio Names'] == "Pretax margin"]['MSE A Index'][13]
            if ptm > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [ptm], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("23.3% of sales turns into profits.")

            st.subheader("Net Profit Margin")
            npm =(state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values) / (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values)
            npm = npm[0]
            mse = mse_index[mse_index['Ratio Names'] == "Net profit margin"]['MSE A Index'][14]
            if npm > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [npm], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("APU works with 23 tugriks profit from 100 turgriks of revenue which is relatively higher than the other peer companies.")

            st.subheader("Return on Asset")
            roa =(state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Asset"]['2020'].values)
            roa = roa[0]
            mse = mse_index[mse_index['Ratio Names'] == "ROA"]['MSE A Index'][15]
            if roa > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [roa], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Return on assets, or ROA, measures how much money a company earns by putting its assets to use. APU is much more efficient and profitable company and they are relative to its assets or the resources it owns or controls.")

            st.subheader("Return on Equity")
            roe =(state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values)
            roe = roe[0]
            mse = mse_index[mse_index['Ratio Names'] == "ROE"]['MSE A Index'][16]
            if roe > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [roe], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Return on equity signifies how good the company is in generating returns on the investment it received from its shareholders. They are doing similar to the average Class 1 company.")

        if ratio == "Valuation Ratios":
            st.header("Valuation Ratios")
            st.write("Valuation ratios measure the quantity of an asset or flow (i.e., earnings) associated with ownership of a specified claim (i.e., a share or ownership of the enterprise).")
            ## Number of shares
            response = requests.get("http://www.mse.mn/mn/company/90")
            soup = BeautifulSoup(response.content)
            result = soup.find_all("div", {"class": "col-lg-6 col-md-6"})
            shares_outstanding = soup.find_all('b')[6].text
            shares_outstanding = shares_outstanding.split(",")[0]+shares_outstanding.split(",")[1]+shares_outstanding.split(",")[2]+shares_outstanding.split(",")[3]
            shares_outstanding = int(shares_outstanding)
            ## Price per share
            apu_stock_df = pd.read_csv("apuStock.csv", thousands=",")
            apu_stock_df['date'] = pd.to_datetime(apu_stock_df['date'])
            pps = apu_stock_df[pd.DatetimeIndex(apu_stock_df['date']).year == 2020][-1:]['value'].reset_index()
            pps = pps['value'][0]

            st.subheader("Price-to-Earnings")
            pe = pps / (state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values*1000/shares_outstanding)
            pe = pe[0]
            mse = mse_index[mse_index['Ratio Names'] == "P/E"]['MSE A Index'][17]
            if pe > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [pe], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("This ratio shows what the market is willing to pay today for a stock based on its past or future earnings. The industry average is 22.89 while P/E ratio of APU 7.23 which is decreased by 1.65 from the previous year. This lower ratio could indicate that the current stock price is low relative to earnings.")

            st.subheader("Price-to-Book Value")
            pbv = pps / (balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values*1000/shares_outstanding)
            pbv = pbv[0]
            mse = mse_index[mse_index['Ratio Names'] == "P/BV"]['MSE A Index'][18]
            if pbv > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [pbv], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("P/BV indicates the inherent value of a company and is a measure of the price that investors are ready to pay for a 'nil' growth of the company. APU has a slightly higher P/Bv ratio than the industry average. The company is earning and is expected to earn in the future a high return on its assetsdecreased cash ratio might be indicating that they might face financial difficulties in the near future.")

            st.subheader("Earnings Per Share")
            eps = (state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values*1000) / shares_outstanding
            eps = eps[0]
            mse = mse_index[mse_index['Ratio Names'] == "EPS"]['MSE A Index'][19]
            if eps > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'APU': [eps], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("EPS indicates how much money a company makes for each share of its stock. APU's EPS is much higher than the MSE Index.")
        

        
### SUU
if company == "SUU":
    st.title("SUU LC")
    st.write("Nowadays, as milk and dairy products become a major part of food consumption, dairy production per capita has become one of the key indicators of national development. Suu JSC, one of the first producers of Mongolia have been producing and delivering over 70 different types of ecological products not only to consumers in the city but also to the countryside for the past 62 years.")
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        suu_stock_df = pd.read_csv("suuStock.csv", thousands=",")
        min_date = st.date_input("The first date")
        min_date = pd.to_datetime(min_date)
        
    with col2:
        max_date = st.date_input("The second date")
        max_date = pd.to_datetime(max_date)

    suu_stock_df = pd.read_csv("suuStock.csv", thousands=",")
    suu_stock_df['date'] = pd.to_datetime(suu_stock_df['date'])
    suu_stock_df = suu_stock_df[(suu_stock_df['date'] >= min_date) & (suu_stock_df['date'] <= max_date)]
    fig = px.line(suu_stock_df, x="date", y="value", title="SUU's Stock price overtime", labels={"date": "Date", "value": "Stock price"})
    st.plotly_chart(fig)
    
    with st.expander("Forecast"):
        sheet_selection = ["Balance Sheet", "Income Statement"]
        sheet = st.selectbox("Choose the financial sheet", sheet_selection)

        if sheet == "Balance Sheet":
            st.subheader("Balance Sheet - Forecast")
            if st.button('See as a table'):
                suu_forecast = pd.read_csv("SUU Forecast.csv", thousands=",")
                st.dataframe(suu_forecast)
            suu_forecast = pd.read_csv("SUU Forecast.csv", thousands=",")

            tae = suu_forecast[(suu_forecast['Breakdown'] == "Total Liability") | (suu_forecast['Breakdown'] == "Total Equity")].reset_index().drop(columns="index", axis=1)
            tae = pd.DataFrame.transpose(tae).reset_index()
            tae.columns = tae.iloc[0]
            tae = tae.drop([0], axis=0)
            tae['Breakdown'] = tae['Breakdown'].str[0:4].astype(int)
            fig = px.line(tae, x='Breakdown', y=['Total Liability', 'Total Equity'], title="Total Liability vs Total Equity Forecast (2021-2025)", labels={"Breakdown": "Year", "value": "In thousand tugriks"})
            fig.add_shape(type="line", x0=2021, y0=0, x1=2021, y1=350000000,line=dict(color="MediumPurple",width=3,dash="dot",))
            st.plotly_chart(fig)

            ca = suu_forecast[1:5]
            ca['Average'] = (ca['2015']+ca['2016']+ca['2017']+ca['2018']+ca['2019']+ca['2020']+ca['2021F']+ca['2022F']+ca['2023F']+ca['2024F']+ca['2025F'])/11
            fig = px.bar(ca, x='Breakdown', y='Average', title="Average current asset breakdown")
            st.plotly_chart(fig)

        if sheet == "Income Statement":
            st.subheader("Income Statement - Forecast")
            if st.button('See as a table'):
                suu_forecast_ins = pd.read_csv("SUU Forecast ins.csv", thousands=",")
                st.dataframe(suu_forecast_ins)

            suu_forecast_ins = pd.read_csv("SUU Forecast ins.csv", thousands=",")
            income = suu_forecast_ins[(suu_forecast_ins['Breakdown'] == "Gross Profit") | (suu_forecast_ins['Breakdown'] == "Net Income")].reset_index().drop(columns="index", axis=1)
            income = pd.DataFrame.transpose(income).reset_index()
            income.columns = income.iloc[0]
            income = income.drop([0], axis=0)
            income['Breakdown'] = income['Breakdown'].str[0:4].astype(int)
            fig = px.line(income, x='Breakdown', y=['Gross Profit', 'Net Income'], title="Gross and Net income over time (2021-2025)", labels={"Breakdown": "Year", "value": "In thousand tugriks"})
            fig.add_shape(type="line", x0=2021, y0=0, x1=2021, y1=30000000,line=dict(color="MediumPurple",width=3,dash="dot",))
            st.plotly_chart(fig)

            in_ex = suu_forecast_ins[(suu_forecast_ins['Breakdown'] == "Operating Income") | (suu_forecast_ins['Breakdown'] == "Operating Expense")].reset_index().drop(columns="index", axis=1)
            in_ex = pd.DataFrame.transpose(in_ex).reset_index()
            in_ex.columns = in_ex.iloc[0]
            in_ex = in_ex.drop([0], axis=0)
            in_ex['Breakdown'] = in_ex['Breakdown'].str[0:4].astype(int)
            fig = px.line(in_ex, x='Breakdown', y=['Operating Income', 'Operating Expense'], title="Operating Income vs Expense (2021-2025)", labels={"Breakdown": "Year", "value": "In thousand tugriks"})
            fig.add_shape(type="line", x0=2021, y0=0, x1=2021, y1=20000000,line=dict(color="MediumPurple",width=3,dash="dot",))
            st.plotly_chart(fig)
            
    with st.expander("Ratio Analysis"):
        st.write("All of the calculations are based on data from the MSE index website where official financial reports of the companies are uploaded usually on a quarterly basis. The MSE A index or otherwise the best performing 20 companies out of all other organizations in Mongolia, industry average will be taken whilst excluding companies that are service oriented. The ratios of the company will be assessed based on the industry averages and overall average.")
        
        ratio_selection = ["Activity Ratios", "Liquidity Ratios", "Leverage Ratios", "Profitability Ratios", "Valuation Ratios"]
        ratio = st.selectbox("Choose the ratio type", ratio_selection)

        suu_forecast_ins = pd.read_csv("SUU Forecast ins.csv", thousands=",")
        suu_forecast = pd.read_csv("SUU Forecast.csv", thousands=",")
        mse_index = pd.read_csv("mse index.csv", thousands=",")
        mse_index = mse_index[['Ratio Names', 'MSE A Index']].dropna()

        balance_ratio = suu_forecast[['Breakdown', '2020']].dropna()
        state_ratio = suu_forecast_ins[['Breakdown', '2020']].dropna()

        if ratio == "Activity Ratios":
            st.header("Activity Ratios")
            st.write("Activity ratios measure how efficiently a company performs day-to-day tasks, such as the collection of receivables and management of inventory.")

            st.subheader("Days of Inventory on hand (DOH)")
            doh = 365/((state_ratio[state_ratio['Breakdown'] == "COGS"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Inventory"]['2020'].values))
            doh = doh[0]
            mse = mse_index[mse_index['Ratio Names'] == "Days of inventory on hands (DOH)"]['MSE A Index'][0]
            if doh > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [doh], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("The duration of inventory on hand is low due to high inventory turnover ratio so it was not interpreted. The industry average is high due to differences in product orientation.")

            st.subheader("Days of Sales outstanding (DSO)")
            dso = 365/((state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Accounts Receivable"]['2020'].values))
            dso = dso[0]
            mse = mse_index[mse_index['Ratio Names'] == "Days of Sales outstanding (DSO)"]['MSE A Index'][1]
            if dso > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [dso], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("It takes Suu only approximately 5-6 days to receive payment for its services/products as opposed to the industry average of 48 which is an extreme advantage when it comes to asset utilization ratio.")

            st.subheader("Number of days of Payables")
            apd = 365/((state_ratio[state_ratio['Breakdown'] == "COGS"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Accounts Payable"]['2020'].values))
            apd = apd[0]
            mse = mse_index[mse_index['Ratio Names'] == "Number of days of payables"]['MSE A Index'][2]
            if apd > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [apd], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Suu has a significantly lower ratio of DPO which means they pack back their debt back in time within a timeframe that is considered swift within the industry.")

            st.subheader("Fixed Asset Turnover")
            fat = (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Fixed Asset"]['2020'].values)
            fat = fat[0]
            mse = mse_index[mse_index['Ratio Names'] == "Fixed asset turnover"]['MSE A Index'][3]
            if fat > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [fat], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Compared to the MSE Index of 4.19, Suu’s FA turnover ratio is considerably lower (50% approx.). This indicates that Suu does not generate the majority of its sales from fixed assets and mostly relies on current assets which is inevitable due to the nature of their business direction (commodities).")

            st.subheader("Total Asset Turnover")
            tat = (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Asset"]['2020'].values)
            tat = tat[0]
            mse = mse_index[mse_index['Ratio Names'] == "Total asset turnover"]['MSE A Index'][4]
            if tat > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [tat], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("A company in the utilities sector is more likely to aim for an asset turnover ratio that is between 0.25 and 0.5. However, the industry average is 0.82 which is only a point or two above the average does not indicate serious deficiencies. From this we can infer that the company can sustain itself by converting revenues into assets.")

        if ratio == "Liquidity Ratios":
            st.header("Liquidity Ratios")
            st.write("Liquidity ratios measure the company’s ability to meet its short-term obligations and how quickly assets are converted into cash.")

            st.subheader("Current Ratio")
            cr = (balance_ratio[balance_ratio['Breakdown'] == "Current Asset"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Current Liability"]['2020'].values)
            cr = cr[0]
            mse = mse_index[mse_index['Ratio Names'] == "Current"]['MSE A Index'][5]
            if cr > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [cr], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("The industry average of companies’ current ratio is exceptionally high which points to discrepancies due to categorization assimilation. Therefore, just evaluating the score of the company alone here is sufficient in which case, 3.9 more current assets as opposed to liabilities show that the company has more than enough assets to cover its short term liabilities. But one could also infer that the high number indicates under-utilisation of its current assets.")

            st.subheader("Quick Ratio")
            qr = ((balance_ratio[balance_ratio['Breakdown'] == "Current Asset"]['2020'].values) - (balance_ratio[balance_ratio['Breakdown'] == "Inventory"]['2020'].values)) / (balance_ratio[balance_ratio['Breakdown'] == "Current Liability"]['2020'].values)
            qr = qr[0]
            mse = mse_index[mse_index['Ratio Names'] == "Quick"]['MSE A Index'][6]
            if qr > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [qr], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Despite the lower average, the rapidity of the company’s ability to pay off its current liabilities in the near future or within a small time frame indicates a high current asset amount.")

            st.subheader("Cash Conversion Cycle")
            doh = (365/((state_ratio[state_ratio['Breakdown'] == "COGS"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Inventory"]['2020'].values)))[0]
            dso = (365/((state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Accounts Receivable"]['2020'].values)))[0]
            apd = (365/((state_ratio[state_ratio['Breakdown'] == "COGS"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Accounts Payable"]['2020'].values)))[0]

            ccc = doh + dso - apd
            mse = mse_index[mse_index['Ratio Names'] == "Cash conversion cycle"]['MSE A Index'][7]
            if ccc > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [ccc], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("The cash conversion rate of Suu is much lower compared to the MSE Index. This means they are able to turn their investments and other resources into cash flow from sales much quickly compared to other organizations.")

        if ratio == "Leverage Ratios":
            st.header("Leverage Ratios")
            st.write("Leverage ratios or solvency ratios measure a company’s ability to meet long-term obligations. Subsets of these ratios are also known as “leverage” and “long-term debt” ratios")

            st.subheader("Debt to asset")
            dta =(balance_ratio[balance_ratio['Breakdown'] == "Short-term Debt"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Long-term Liability"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Asset"]['2020'].values)
            dta = dta[0]
            mse = mse_index[mse_index['Ratio Names'] == "Debt to asset"]['MSE A Index'][8]
            if dta > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [dta], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("The industry average debt to asset ratio of companies is quite low at 0.18. Suu LLC’s ratio is 0.47 which may be higher than the average yet still cannot be considered a weak point as it falls within an acceptable range. This means their unpaid debts are not too high and does not constitute the majority of its assets.")

            st.subheader("Debt to capital")
            dtc =(balance_ratio[balance_ratio['Breakdown'] == "Short-term Debt"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Long-term Liability"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Short-term Debt"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Long-term Liability"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values)
            dtc = dtc[0]
            mse = mse_index[mse_index['Ratio Names'] == "Debt to capital"]['MSE A Index'][9]
            if dtc > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [dtc], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("There is no useful inference to be made here whilst comparing to the industry average. The category of each company varies with such a range that it cannot be deemed as a standard when it comes to this ratio. Suu, being a commodity product/food and beverage manufacturer relies heavily on its plants, products and current assets. They have a ratio of 0.56 which is considerably higher than the industry average. But the only information here is that the company itself has a decent rate of debt to capital conversion.")

            st.subheader("Debt to equity")
            dte =(balance_ratio[balance_ratio['Breakdown'] == "Short-term Debt"]['2020'].values + balance_ratio[balance_ratio['Breakdown'] == "Long-term Liability"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values)
            dte = dte[0]
            mse = mse_index[mse_index['Ratio Names'] == "Debt to equity"]['MSE A Index'][10]
            if dte > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [dte], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("The debt to equity ratio of Suu is rather larger compared to the industry average, indicatingsome reliance on debts rather than fully exclusive assets. But it is still within acceptable rangeand should not hurt the company’s current and future performance.")

            st.subheader("Financial Leverage")
            fl = balance_ratio[balance_ratio['Breakdown'] == "Total Asset"]['2020'].values / balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values
            fl = fl[0]
            mse = mse_index[mse_index['Ratio Names'] == "Financial leverage"]['MSE A Index'][11]
            if fl > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [fl], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Though it is stated above that this ratio will be tolerated at higher level, it is still notable to understand that the average of the company is higher compared to the industry average. This means the majority of its total asset is not fully owned (owner’s equity).")        

        if ratio == "Profitability Ratios":
            st.header("Profitability Ratios")
            st.write("Profitability ratios measure the company’s ability to generate profits from its resources (assets).")

            st.subheader("Gross Profit Margin")
            gpm =(state_ratio[state_ratio['Breakdown'] == "Gross Profit"]['2020'].values) / (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values)
            gpm = gpm[0]
            mse = mse_index[mse_index['Ratio Names'] == "Gross profit margin"]['MSE A Index'][12]
            if gpm > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [gpm], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("The revenue retention rate of Suu is 0.29, slightly higher than the industry average. The company keeps a higher amount of revenue compared to other companies after it has covered all its business expenses.")

            st.subheader("Pretax Margin")
            ptm =(state_ratio[state_ratio['Breakdown'] == "EBT"]['2020'].values) / (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values)
            ptm = ptm[0]
            mse = mse_index[mse_index['Ratio Names'] == "Pretax margin"]['MSE A Index'][13]
            if ptm > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [ptm], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Suu LLC’s 2019 pretax margin was 9% and did not change significantly since then. The takeaway is the improvement of its profits before taxes shows that the company is increasing its profitability.")

            st.subheader("Net Profit Margin")
            npm =(state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values) / (state_ratio[state_ratio['Breakdown'] == "Sales"]['2020'].values)
            npm = npm[0]
            mse = mse_index[mse_index['Ratio Names'] == "Net profit margin"]['MSE A Index'][14]
            if npm > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [npm], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Suu has a slightly lower ability compared to other companies when it comes to revenue conversion into profit.")

            st.subheader("Return on Asset")
            roa =(state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Asset"]['2020'].values)
            roa = roa[0]
            mse = mse_index[mse_index['Ratio Names'] == "ROA"]['MSE A Index'][15]
            if roa > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [roa], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Suu is slightly above the industry average at 8.9% which is 0.8% higher.")

            st.subheader("Return on Equity")
            roe =(state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values) / (balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values)
            roe = roe[0]
            mse = mse_index[mse_index['Ratio Names'] == "ROE"]['MSE A Index'][16]
            if roe > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [roe], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("One of the most important ratios and the defining characteristic of profitability of a company. Considering the industry average of nearly 19% and Suu LLC’s ROE of 19.6%, it is clear that Suu has more than adequate handling of its equity and beneficial conditions for stockholders by offering a higher return on it.")

        if ratio == "Valuation Ratios":
            st.header("Valuation Ratios")
            st.write("Valuation ratios measure the quantity of an asset or flow (i.e., earnings) associated with ownership of a specified claim (i.e., a share or ownership of the enterprise).")
            ## Number of shares
            response = requests.get("http://www.mse.mn/mn/company/90")
            soup = BeautifulSoup(response.content)
            result = soup.find_all("div", {"class": "col-lg-6 col-md-6"})
            shares_outstanding = soup.find_all('b')[6].text
            shares_outstanding = shares_outstanding.split(",")[0]+shares_outstanding.split(",")[1]+shares_outstanding.split(",")[2]+shares_outstanding.split(",")[3]
            shares_outstanding = int(shares_outstanding)
            ## Price per share
            suu_stock_df = pd.read_csv("suuStock.csv", thousands=",")
            suu_stock_df['date'] = pd.to_datetime(suu_stock_df['date'])
            pps = suu_stock_df[pd.DatetimeIndex(suu_stock_df['date']).year == 2020][-1:]['value'].reset_index()
            pps = pps['value'][0]

            st.subheader("Price-to-Earnings")
            pe = pps / (state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values*1000/shares_outstanding)
            pe = pe[0]
            mse = mse_index[mse_index['Ratio Names'] == "P/E"]['MSE A Index'][17]
            if pe > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [pe], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("This ratio shows what the market is willing to pay today for a stock based on its past or future earnings. The industry average is 22.89 while P/E ratio of SUU 35.1. This higher ratio could indicate that the current stock price is high relative to earnings.")

            st.subheader("Price-to-Book Value")
            pbv = pps / (balance_ratio[balance_ratio['Breakdown'] == "Total Equity"]['2020'].values*1000/shares_outstanding)
            pbv = pbv[0]
            mse = mse_index[mse_index['Ratio Names'] == "P/BV"]['MSE A Index'][18]
            if pbv > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [pbv], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("Traditionally, any value under 1.0 is considered a good P/B value, indicating a potentially undervalued stock. Since the ratio is higher than 1, the stock price might be overvalued.")

            st.subheader("Earnings Per Share")
            eps = (state_ratio[state_ratio['Breakdown'] == "Net Income"]['2020'].values*1000) / shares_outstanding
            eps = eps[0]
            mse = mse_index[mse_index['Ratio Names'] == "EPS"]['MSE A Index'][19]
            if eps > mse:
                analysis = "Higher"
            else:
                analysis = "Lower"
            data = {'SUU': [eps], 'MSE A Index': [mse], 'Analysis': [analysis]}
            ratiodf = pd.DataFrame(data=data)
            st.dataframe(ratiodf)
            st.write("EPS indicates how much money a company makes for each share of its stock. SUU's EPS is much lower than the MSE Index.")
            
