# -*- coding: utf-8 -*-
"""Stock Prediction ARIMA Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1k31oCoBjyagmJYqy0LMx1YIAiNX9STPR
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # graphing

!pip install yfinance

import yfinance as yf # for financial data

df = yf.download("^GSPC", period="5y", interval="1d")
df

df = df.asfreq('D')
df

df = df.fillna(method='ffill')
df

# filter columns
ts = df[['Close']]
ts

# Plot the data and identify any unusual observations
plt.figure(figsize=(10, 6))
plt.plot(ts.index, ts.values, label='Original Data')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

# Perform seasonal decomposition
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ts, model='additive')

trend = decomposition.trend
seasonal = decomposition.seasonal
residuals = decomposition.resid

# Create subplots for each component
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 8))

# Plot the original time series
axes[0].plot(ts, label='Original')
axes[0].set_ylabel('Original')

# Plot the trend component
axes[1].plot(trend, label='Trend')
axes[1].set_ylabel('Trend')

# Plot the seasonal component
axes[2].plot(seasonal, label='Seasonality')
axes[2].set_ylabel('Seasonality')

# Plot the residuals component
axes[3].plot(residuals, label='Residuals')
axes[3].set_ylabel('Residuals')

# Add titles and legends
axes[0].set_title('Time Series Decomposition')
plt.tight_layout()
plt.show()

from statsmodels.tsa.stattools import adfuller

# Augmented Dickey-Fuller (ADF) Test
result = adfuller(ts)

# Extract p-value from the result
p_value = result[1]

print(p_value)

!pip install pmdarima

from pmdarima.arima.utils import ndiffs

ndiffs(ts, test="adf")

from statsmodels.tsa.stattools import adfuller

# Augmented Dickey-Fuller (ADF) Test
result = adfuller(ts.Close.diff().dropna())

# Extract p-value from the result
p_value = result[1]

print(p_value)

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

# Plot ACF
fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(ts.Close.diff().dropna(), lags=20, ax=ax)  # Specify the number of lags to display
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation Function (ACF)')
plt.show()

# Plot PACF
fig, ax = plt.subplots(figsize=(10, 6))
plot_pacf(ts.Close.diff().dropna(), lags=20, ax=ax)  # Specify the number of lags to display
plt.xlabel('Lag')
plt.ylabel('Partial Autocorrelation')
plt.title('Partial Autocorrelation Function (PACF)')
plt.show()

# train/test split
ts_train = ts.iloc[:int(ts.size * .8)]
ts_test = ts.iloc[int(ts.size * .8):]

# Plot the data and identify any unusual observations
plt.figure(figsize=(10, 6))
plt.plot(ts_train.index, ts_train.values, label='Train Data')
plt.plot(ts_test.index, ts_test.values, 'green', label='Test Data')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

import pmdarima as pm

# Fit the ARIMA model
model = pm.auto_arima(ts_train, seasonal=True)
model.summary()

from statsmodels.tsa.arima.model import ARIMA

# Fit ARIMA model
model = ARIMA(ts_train.values, order=(0, 1, 1))  # Replace p, d, q with appropriate values
model = model.fit()

residuals = pd.DataFrame(model.resid)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

ax1.plot(residuals)
ax2.hist(residuals, density=True)

# Forecast
forecast_steps = int(ts.size) - int(ts.size * .8)  # Number of future time steps to forecast

forecast = model.forecast(steps=forecast_steps)

# Plot the data and identify any unusual observations
plt.figure(figsize=(10, 6))
plt.plot(ts_train.index, ts_train.values, 'blue', label='Train Data')
plt.plot(ts_test.index, ts_test.values, 'green', label='Test Data')
plt.plot(ts_test.index, forecast, 'orange', label='Forecasted Data')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

# Plot the original data and forecasted values
plt.figure(figsize=(10, 6))
plt.plot(ts_test.index, ts_test.values, label='Original Data')
plt.plot(ts_test.index, forecast, label='Forecasted Data')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('ARIMA Forecast')
plt.show()

ts_test

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Generate predictions for the test data
forecast_steps = len(ts_test)
forecast = model.forecast(steps=forecast_steps)

# Compute accuracy metrics
mae = mean_absolute_error(ts_test, forecast)
mse = mean_squared_error(ts_test, forecast)
rmse = np.sqrt(mse)

print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)

print("Length of ts_test:", len(ts_test))
print("Length of forecast:", len(forecast))

print("Data type of ts_test:", type(ts_test))
print("Data type of forecast:", type(forecast))
print("ts_test values:", ts_test)
print("forecast values:", forecast)

# Convert DataFrame to NumPy array
ts_test_values = ts_test['Close'].values

# Calculate absolute percentage errors
abs_percentage_errors = np.abs((ts_test_values - forecast) / ts_test_values)

# Calculate MAPE
mape = np.mean(abs_percentage_errors) * 100

print("Mean Absolute Percentage Error (MAPE):", mape)