import statsmodels.api as sm
import pandas as pd
from datetime import timedelta

def rolling_arima(series, periods):
    model = sm.tsa.ARIMA(series, order=(5,1,0))
    fit = model.fit()
    return fit.forecast(steps=periods)

def apply_forecast(df, periods):
    forecasts = []
    for sku in df['SKU'].unique():
        sku_df = df[df['SKU']==sku].set_index('Date').sort_index()
        f = rolling_arima(sku_df['Sales'], periods)
        idx = pd.date_range(start=sku_df.index.max()+timedelta(days=1),
                            periods=periods, freq='M')
        forecasts.append(pd.DataFrame({'Date':idx, 'SKU':sku, 'Forecast':f}))
    return pd.concat(forecasts)

