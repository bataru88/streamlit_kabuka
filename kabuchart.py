#OverView
#############################################################
#streamlit学習
#株価可視化アプリ
#Yahooファイナンスから株式情報を取得して表示する。
#米国株式市場におけるGAFAの株価を表示したアプリケーションを表示する。

#学ぶこと
#yfinanceを用いた株式情報の取得
#Altairを用いたグラフの作り方
##############################################################

import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

#株価情報の取得対象
tickers = {
    'apple':'AAPL',
    'facebook':'FB',
    'google':'GOOGL',
    'microsoft':'MSFT',
    'netflix':'NFLX',
    'amazon':'AMZN'
}

st.title('米国株価可視化アプリ')

st.sidebar.write("""
    # GAFA株価
     こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
     """)

st.sidebar.write("""
    ##　表示日数選択
    """)
days = st.sidebar.slider('日数',1,50,20)

st.sidebar.write("""
    ##　株価の範囲指定
    """)
ymin,ymax = st.sidebar.slider('範囲を指定してください',0.0,3500.0,(0.0,3500.0))

st.write(f"""
    ### 過去 **{days}日間** のGAFA株価
    """)

@st.cache
#株価情報の取得
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():

        #ティッカーシンボルの指定
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')

        #indexの日付の書式を変更する ⇨　d Month year
        hist.index = hist.index.strftime('%d %B %Y')
        #終値(close)を使用する。
        hist = hist[['Close']]
        hist.columns = [company]
        #"転置"
        hist = hist.T
        #Indexに名前をつける
        hist.index.name = 'Name'
        #テーブルにデータを追加
        df = pd.concat([df,hist])
    return df

try:
    df = get_data(days, tickers)

    companies = st.multiselect(
        '会社名を洗濯してください',
        list(df.index),
        ['google','amazon','facebook','apple']
    )
    if not companies:
        st.error('少なくとも一社は選んでください')
    else:
        data = df.loc[companies]
        st.write("### 株価(USD)",data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns = {'value':'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8,clip=True)
            .encode(
                x ="Date:T",
                y =alt.Y("Stock Prices(USD):Q" , stack=None,scale=alt.Scale(domain=[ymin,ymax])),
                color='Name:N'          
            )
        )
        st.altair_chart(chart,use_container_width=True)
except:
    st.error(
        """なんかエラーでとるぞ！"""
    )
















