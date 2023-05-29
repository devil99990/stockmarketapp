import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

#image at starting 
from PIL import Image
st.set_page_config(layout="wide")
img = Image.open("stockh.jpg")
Image = img.resize((1400, 300))
st.image(Image)

START = "2000-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Sidebar
st.sidebar.title('Navigation')
options = ['Stock Forecast', 'About', 'News', 'Study Videos']
selection = st.sidebar.radio('Go to', options)
default_index=0,  # optional
orientation="horizontal",

# About page
if selection == 'About':
    st.title('About')
    st.write('This app predicts the future prices of the stocks.')

    st.write('Built with Streamlit and the Prophet library.')

# News page
elif selection == 'News':
    st.title('News')
    st.write('Latest news about the stock market will be displayed here.')
    # Add your code to fetch and display news articles here.

# Study Videos page
elif selection == 'Study Videos':
    st.title('Study Videos')
    st.write('Videos about stock market analysis and prediction will be displayed here.')
    # Add your code to display study videos here.

# Stock Forecast page
else:
    
    selected_stock  = st.text_input('Pick Stock here ','TCS.NS')

    link = "https://finance.yahoo.com/"
    st.text(" Pick Stock name  from  Yahoo Finance in the format like  INFY.NS ")
    st.write(" Yahoo Finance Portal Link for correct name of stock   :  [link](%s)" % link)

    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365

    @st.cache
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
