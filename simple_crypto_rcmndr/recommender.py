import math
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


crypto_data = pd.read_csv('crypto_data.csv')

scaler = MinMaxScaler()
crypto_data[[
     'id'
     'market_cap',
     'trading_volume',
     'price',
     'volatility']] = scaler.fit_transform(crypto_data[[
                                                'Market Cap',
                                                'Volume(24h)',
                                                'Price',
                                                '1h %']])

sort = input('sort importance (market cap:M, trading vol:T, price:P, volatility:V)(e.g MTPV , M is most important):')

M = 1
T = 1
P = 1
V = 1

if sort[0] == 'M':
    M=4
elif sort[0] == 'T':
    T=4
elif sort[0] == 'P':
    P=4
elif sort[0] == 'V':
    V=4
if sort[1] == 'M':
    M=2
elif sort[1] == 'T':
    T=2
elif sort[1] == 'P':
    P=2
elif sort[1] == 'V':
    V=2

# Get P of each atrribute
market_cap_P = ((crypto_data['Market Cap']) / crypto_data['Market Cap'].sum()) ** 0.33
trading_volume_P = (crypto_data['trading_volume'] / crypto_data['trading_volume'].sum()) ** 0.33
price_P = ( ((crypto_data['price']) / crypto_data['price'].median()) ** 0.16)
volatility_P = (crypto_data['volatility'].max() / crypto_data['volatility']) ** 1.25


# Calculate score for each cryptocurrency
crypto_data['score'] = (M*market_cap_P + T*trading_volume_P) * P*price_P * T*volatility_P

top_cryptos = crypto_data.nlargest(5, 'score')
for i, row in top_cryptos.iterrows():
    if  math.isinf(row['score']):
        crypto_data.loc[i, 'score'] = 0.0144

top_cryptos = crypto_data.nlargest(5, 'score')
print('Top 5 recommended CryptoCurrencies:')
for i, row in top_cryptos.iterrows():
    print(f"{row['Name']}: Score - {row['score']:.2f}")

