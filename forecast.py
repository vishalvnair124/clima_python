import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from io import StringIO
import pickle

# Load the fitted models from pickle file
with open('arima_models.pkl', 'rb') as f:
    loaded_models = pickle.load(f)

# Sample 7-day data
sample_data = """
Date,Temperature,Humidity,Pressure,CO,SO2,NO2,PM 2.5
2024-02-15 17:56:10,25.17,51,1012,2.53,0.64,14.08,16.39
2024-02-19 18:40:43,29.95,57,1019,1.56,1.29,14.22,17.63
2024-03-04 15:56:46,22.44,47,1003,1.97,1.21,12.66,14.66
2024-03-05 02:25:15,28.04,66,1012,2.39,0.89,12.88,18.96
2024-02-13 12:10:30,26.29,41,1004,2.92,0.52,12.73,14.5
2024-02-20 12:00:25,24.38,66,1005,1.67,1.29,14.67,18.48
2024-02-09 03:20:07,26.12,63,1000,2.33,1.16,11.14,11.44
"""

# Convert sample data string to DataFrame
sample_df = pd.read_csv(StringIO(sample_data), parse_dates=['Date'], index_col='Date')

# Forecast future values for each variable using the loaded ARIMA models
forecasts = {}
for variable, model in loaded_models.items():
    forecasts[variable] = model.forecast(steps=len(sample_df))

# print("Forecasts:")
# for variable, forecast_values in forecasts.items():
#     print(f"{variable}: {forecast_values}")

def get_forecast_weather():
    result = {
        "CO2": forecasts['CO'],
        "PM25": forecasts['PM 2.5'],
        "SO2": forecasts['SO2'],
        "NO2": forecasts['NO2'],
        "Temperature": forecasts['Temperature'],
    }
    return result

# Call the function to get forecasted values
forecasted_values = get_forecast_weather()
# print("\nForecasted Values:")
# print(forecasted_values)
