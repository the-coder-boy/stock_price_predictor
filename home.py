import numpy as np
import pandas as pd
import yfinance as yf
from keras.models import load_model 
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Home", page_icon="📈")

model=load_model('Stock Prediction Model.keras')

model=load_model('Stock Prediction Model.keras')

st.title('Stock Market Predictor')

st.sidebar.success("Menu")

stock=st.text_input('Enter Stock Tinker','GOOG')
start='2015-01-01'
end='2024-09-30'

data=yf.download(stock,start,end)

st.header('Stock Data')
st.write(data)

data_train=pd.DataFrame(data.Close[0: int(len(data)*0.80)])
data_test=pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))

pas_100_days=data_train.tail(100)
data_test=pd.concat([pas_100_days,data_test],ignore_index=True)
data_test_scale=scaler.fit_transform(data_test)

st.subheader('Price vs Moving Average 50 Days')
ma_50_days=data.Close.rolling(50).mean()
fig1=plt.figure(figsize=(10,8))
plt.plot(ma_50_days,'r')
plt.plot(data.Close,'g')
plt.show()
st.pyplot(fig1)

st.subheader('Price vs Moving Average 50 Days vs Moving Average 100 Days')
ma_100_days=data.Close.rolling(100).mean()
fig2=plt.figure(figsize=(10,8))
plt.plot(ma_50_days,'r')
plt.plot(ma_100_days,'b')
plt.plot(data.Close,'g')
plt.show()
st.pyplot(fig2)

st.subheader('Price vs Moving Average 100 Days vs Moving Average 200 Days')
ma_200_days=data.Close.rolling(200).mean()
fig3=plt.figure(figsize=(10,8))
plt.plot(ma_100_days,'r')
plt.plot(ma_200_days,'b')
plt.plot(data.Close,'g')
plt.show()
st.pyplot(fig3)

x=[]
y=[]
for i in range(100,data_test_scale.shape[0]):
    x.append(data_test_scale[i-100:i])
    y.append(data_test_scale[i,0])

x,y=np.array(x),np.array(y)

predict=model.predict(x)

scale=1/scaler.scale_

predict=predict*scale
y=y*scale

st.subheader('Original Price vs Predicted Price')
ma_100_days=data.Close.rolling(100).mean()
fig4=plt.figure(figsize=(8,6))
plt.plot(predict,'r',label='Original Price')
plt.plot(y,'b',label='Predictedd Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
st.pyplot(fig4)

# limiting the predicted values for last 30 days only
predict = predict[-30:]
dataRequired = data['Close'].iloc[-30:]

# Buy, Sell, Keep logic
def get_opinion(predicted, actual,previous_actual, buy_threshold=0.01, sell_threshold=-0.01):
    percentage_diff = (predicted - actual) / actual  
    
    # Adding a trend check based on the previous day's price        
    trend = (actual - previous_actual) / previous_actual
    
    # Buy if the trend is positive 
    if percentage_diff > buy_threshold and trend > 0:
        return "Buy"
    # Sell if the trend is negative 
    elif percentage_diff < sell_threshold and trend < 0:
        return "Sell"

    else:
        return "Keep"


st.write("Stock Predictions and Opinions")

# Slider 
num_days = st.slider('Select number of days to show opinions:', min_value=1, max_value=30, value=5)

# Generate opinions for each predicted value
l = []
for i in range(num_days):
    actual_price = dataRequired.iloc[i]
    predicted_price = predict[i][0]
    previous_actual_price = dataRequired.iloc[i - 1] if i > 0 else actual_price
    l.append(predicted_price)

main_maxima = max(l) #certain selling point
index_maxima = l.index(main_maxima)
l_certainty = []#certain rangee
for i in range(0,index_maxima+1):
    l_certainty.append(l[i])
certain_minima = min(l_certainty) #certain buyingpoint
inndexof_buying = l.index(certain_minima)
l_uncertain = []#ucertain range
for i in range(index_maxima,len(l)):
    l_uncertain.append(l[i])
uncertain_minima = min(l_uncertain)#uncertain minima
un_min_index = l_uncertain.index(uncertain_minima)#index of uncertain minima
credibility_un = []
for i in range(un_min_index,len(l_uncertain)):
    credibility_un.append(l_uncertain[i])
miniature_profit = max(credibility_un)

#finding index of uncertain minima in primary list
for i in range(index_maxima,len(l)):
    if l[i] == uncertain_minima:
        indexof_uncertainminima = i
    if l[i] == miniature_profit:
        indexof_miniprofit = i

for i, predicted_price in enumerate(l):
    if i == index_maxima:
        st.write(f"Day {i+1}: Predicted Price = {predicted_price}, Opinion = Sell")
    elif i == inndexof_buying:
       
       st.write(f"Day {i+1}: Predicted Price = {predicted_price}, Opinion = Buy")
    else:
        if indexof_miniprofit == indexof_uncertainminima:
            st.write(f"Day {i+1}: Predicted Price = {predicted_price}, Opinion = Keep")
        elif indexof_miniprofit == i:
            st.write(f"Day {i+1}: Predicted Price = {predicted_price}, Opinion = Sell")
        elif indexof_uncertainminima == i:
            st.write(f"Day {i+1}: Predicted Price = {predicted_price}, Opinion = Buy")
        else:
            st.write(f"Day {i+1}: Predicted Price = {predicted_price}, Opinion = Keep")

st.subheader('Predicted Price')
fig5=plt.figure(figsize=(8,6))
plt.plot(l,'b',label='Predicted Price',linestyle='dashed')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
st.pyplot(fig5)
