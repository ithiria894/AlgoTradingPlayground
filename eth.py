import ccxt
import pandas as pd
import streamlit as st

# Initialize ccxt and set up Binance exchange
exchange = ccxt.binance()

# Fetch ETH/USDT monthly OHLCV data
ohlcv = exchange.fetch_ohlcv('ETH/USDT', timeframe='1M', since=exchange.parse8601('2017-01-01T00:00:00Z'))

# Convert data to DataFrame
eth_data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Convert timestamp to datetime and set it as the index
eth_data['timestamp'] = pd.to_datetime(eth_data['timestamp'], unit='ms')
eth_data.set_index('timestamp', inplace=True)

# Extract year and month
eth_data['year'] = eth_data.index.year
eth_data['month'] = eth_data.index.month

# 1. Max Drawdown (Low to Open)
eth_data['max_drawdown'] = (eth_data['low'] - eth_data['open']) / eth_data['open'] * 100

# Create pivot table for max drawdown by year and month
pivot_table_drawdown = eth_data.pivot_table(values='max_drawdown', index='year', columns='month', aggfunc='min')

# Calculate mean and median of max drawdown by year
avg_drawdown = pivot_table_drawdown.mean(axis=0)
median_drawdown = pivot_table_drawdown.median(axis=0)

# Add mean and median for the drawdown table
pivot_table_drawdown.loc['Avg'] = avg_drawdown
pivot_table_drawdown.loc['Median'] = median_drawdown

# 2. High to Open % Change (Open to High)
eth_data['high_to_open_change'] = (eth_data['high'] - eth_data['open']) / eth_data['open'] * 100
pivot_table_high_change = eth_data.pivot_table(values='high_to_open_change', index='year', columns='month', aggfunc='mean')

# Calculate mean and median of high to open change by year
avg_change = pivot_table_high_change.mean(axis=0)
median_change = pivot_table_high_change.median(axis=0)

# Add mean and median for the high to open change table
pivot_table_high_change.loc['Avg'] = avg_change
pivot_table_high_change.loc['Median'] = median_change

# 3. Monthly Returns (Open to Close)
eth_data['monthly_return'] = (eth_data['close'] - eth_data['open']) / eth_data['open'] * 100
pivot_table_monthly_return = eth_data.pivot_table(values='monthly_return', index='year', columns='month', aggfunc='mean')

# Calculate mean and median of monthly returns by year
avg_return = pivot_table_monthly_return.mean(axis=0)
median_return = pivot_table_monthly_return.median(axis=0)

# Add mean and median for the monthly return table
pivot_table_monthly_return.loc['Avg'] = avg_return
pivot_table_monthly_return.loc['Median'] = median_return

# Styling function for tables
def style_table(pivot_table):
    return pivot_table.style \
        .format('{:.2f}%') \
        .set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]},  # Header background color and font
            {'selector': 'tbody td', 'props': [('text-align', 'center'), ('color', 'black')]},  # Table data color
            {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#f2f2f2')]},  # Odd row background color
            {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#ffffff')]},  # Even row background color
            {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]},  # Table width
            {'selector': 'th', 'props': [('padding', '8px')]},  # Header cell padding
            {'selector': 'td', 'props': [('padding', '8px'), ('border', '1px solid #ddd')]},  # Data cell padding and border
        ]) \
        .set_table_attributes('class="dataframe"')  # Add class for styling

# Streamlit Display
st.title('ETH/USDT Data Analysis (Max Drawdown, Open to High Change, Monthly Return)')

# Display the Max Drawdown table
st.subheader("Max Drawdown (Low to Open) by Year and Month")
st.write(pivot_table_drawdown,use_container_width=True)

# Display the Open to High Change table
st.subheader("Open to High % Change by Year and Month")
st.write(pivot_table_high_change,use_container_width=True)

# Display the Monthly Returns table
st.subheader("Monthly Returns (Open to Close) by Year and Month")
st.write(pivot_table_monthly_return,use_container_width=True)

