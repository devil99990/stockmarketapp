import streamlit as st
from datetime import date
import pandas as pd 
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
from newsapi import NewsApiClient
import datetime
from urllib.request import urlopen
from io import BytesIO
import requests
#image at strating 
from PIL import Image
st.set_page_config(layout="wide")
#img = Image.open("stockh.jpg")
link = "https://finance.yahoo.com/"
# display image using streamlit
# width is used to set the width of an image
#st.image(img, width=900)
img = Image.open("stockh.jpg")
Image = img.resize((1400, 300))
st.image(Image)
# Sidebar
st.sidebar.title('HOME')
options = ['Stock Forecast', 'News', 'Study Videos','About']
selection = st.sidebar.radio('Select below options to explore more', options)
default_index=0,  # optional
orientation="horizontal",

if selection == 'Stock Forecast':
    #st.title('Stock Forecast')
    # start date
    START = "2000-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title('Stock Forecast App 💵📊📈📢')

    selected_stock  = st.text_input('Pick Stock here ','TCS.NS')

    st.text(" Pick Stock name  from  Yahoo Finance in the format like  INFY.NS ")
    st.write(" Yahoo Finance Portal Link for correct name of stock   :  [link](%s)" % link)


        #stocks = ('INFY.NS','TATAMOTORS.NS', 'TCS.NS', 'RELIANCE.NS','HDFCBANK.NS','WIPRO.NS')

    #selected_stock = st.selectbox('Select dataset for prediction', stocks)
    START = "2000-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365




    @st.cache
#@st.cache_resource
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data


    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data... done!✅')
    
    st.subheader('Raw data till date 📊🎰 ')
    st.table(data.tail())
# Plot raw data
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    #st.subheader()
        fig.layout.update(title_text='Time Series Data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)


    plot_raw_data()

# Predict forecast with Prophet.
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

# Show and plot forecast
    st.subheader('Forecast Data')
    st.write(forecast.tail())

    st.subheader(f'Forecast Plot For {n_years} Years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast Components For Treand,Week and Year ")
    fig2 = m.plot_components(forecast)
    st.write(fig2)


#newsapi = NewsApiClient(api_key='bb849a81fac24291bf2f6fe9aa9899d9')

newsapi = NewsApiClient(api_key='bb849a81fac24291bf2f6fe9aa9899d9')

if selection == 'News':
    st.title('News')
    
    # Get the top headlines from the NewsAPI
    top_headlines = newsapi.get_top_headlines( language='en', country='in', category='business',page_size=100 )
    
    
    if top_headlines['status'] == 'ok':
        articles = top_headlines['articles']
        
        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            image_url = article['urlToImage']
            
            # Display the article image
            st.image(image_url, caption=title, use_column_width=True)
            
            # Display the article details
            st.write(title)
            st.write(description)
            st.write(url)
            st.write('\n')
    else:
        st.write('Error fetching articles')
        st.write(top_headlines['message'])


elif selection == 'Study Videos':
   
    st.title('Study Videos')
    st.write('Videos about stock market analysis and prediction for beginners to advanced level.')

# Beginner Level Videos
    st.header('Beginner Level')
    st.subheader('1. Introduction to Stock Market')
    st.video('https://www.youtube.com/watch?v=bYd6QY5ZGtY&list=PLDN4K7xX0ZHWAYMrdh4oqJpdZGFdCQf-O')

    st.subheader('2. Understanding Stock Market Basics')
    st.video('https://youtu.be/3UF0ymVdYLA')

# Intermediate Level Videos
    st.header('Intermediate Level')
    st.subheader('1. Technical Analysis in Stock Trading')
    st.video('https://youtu.be/mRfVY9Wbnrs')

    st.subheader('2. Fundamental Analysis of Stocks')
    st.video('https://www.youtube.com/watch?v=PQqfeyUQbyE&list=PL8uhW8cclMiOFY9hUCP7uROKCLkIMQ1tI')

# Advanced Level Videos
    st.header('Advanced Level')
    st.subheader('1. Options Trading Strategies')
    st.video('https://www.youtube.com/watch?v=nP9IMTKIl2w&list=PLxNHpNhDaEFLTT826yucpRLr6TAMSKziU')

    st.subheader('2. Algorithmic Trading in Python')
    st.video('https://youtu.be/7G6zIoQc4rk')

# Additional Resources
    st.header('Additional Resources')
    st.subheader('1. Stock Market Courses')
    st.write('Check out popular online courses such as Udemy, Coursera, and LinkedIn Learning for comprehensive stock market courses.')

    st.subheader('2. Books on Stock Market Analysis')
    st.write('Here are some recommended books for in-depth understanding of stock market analysis:')
    st.write('1. "One Up on Wall Street" by Peter Lynch')
    st.write('2. "Let’s talk money" by Monika Halan')
    st.write('3. "Rich Dad Poor Dad" by Robert T Kiyosaki')
    st.write('4. "The little book that beats the market" by Joel GreenBlatt')
    st.write('5. "Diamonds in the dust" by Salil Desai')
    st.write('6. "The unusual billionaires" by Saurabh Mukerjea')
    st.write('7. "Bulls, bears and other beasts" by Santhosh Nair')
    st.write('8. "Trade like a stock market wizard" by Mark Menervini')
    st.write('9. "The Warren Buffet way" by Robert G Hagstrom')
 
   
    st.subheader('3. Online Stock Market Forums')
    st.write('Engage with the stock market community and gain insights on Indian stock market forums:')
    st.write('- Moneycontrol Forum: [Link](https://mmb.moneycontrol.com/forum-topics/stocks)')
    st.write('- ValuePickr Forum: [Link](https://forum.valuepickr.com/c/stock-ideas/7)')
    st.write('- Traderji Forum: [Link](https://www.traderji.com/community/forums/stock-market.7/)')


    st.subheader('4. Financial News Websites')
    st.write('Stay updated with the latest financial news and analysis on the following websites:')
    st.write('- Moneycontrol: [Link](https://www.moneycontrol.com/)')
    st.write('- Economic Times: [Link](https://economictimes.indiatimes.com/)')
    st.write('- NDTV Profit: [Link](https://www.ndtv.com/business)')
    st.write('- CNBC TV18: [Link](https://www.cnbc.com/cnbc-tv18/)')
# Add more study resources as needed
if selection == 'About':
    #st.title('About us ')
    st.title("About the Stock Market Prediction Web App")
    st.write("This Stock Market Prediction Web App is developed by a group of students from GS Raisoni College of Engineering, Nagpur, in the Department of Information Technology.")
    st.write("The team members involved in the development of the web app are:")
    st.write("1. Aniket Wasnik")
    st.write("2. Anshul Chaudhari")
    st.write("3. Abhishek Khasre")
    st.write("4. Chetan Kaware")
    st.write("5. Abhishek Kondalkar")
    st.write("6. Rajesh Nakhate")
    st.write("The web app aims to provide users with predictions and insights into the stock market. It leverages various techniques and algorithms to analyze historical stock data and generate predictions for future market trends.")
    st.write("Users can input specific stocks or market indices and receive predictions, recommendations, and visualizations to assist them in making informed investment decisions.")
    st.write("The team has implemented features such as historical data analysis, technical indicators, machine learning models, and interactive visualizations to enhance the user experience and provide valuable insights into the stock market.")
    st.write("The web app strives to be user-friendly, intuitive, and informative, catering to both beginner and advanced users in the field of stock market investing.")
    st.title("Disclaimer:")
    st.write(" Stock market predictions are based on historical data and statistical models, and there is no guarantee of accuracy or success in stock market trading. Users are advised to conduct their own research and consult with financial professionals before making any investment decisions.")









