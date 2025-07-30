import pandas as pd
import yaml
from src.extract import extract_data
from src.transform import aggregate, merge_with_input
from src.forecast import apply_forecast

def load_config():
    return yaml.safe_load(open('config/config.yaml'))

def main():
    cfg = load_config()

    # 1) Extraer datos de SharePoint
    raw = extract_data()

    # 2) Merge con lista de precios
    price_df = pd.read_csv(cfg['prices']['file'])
    # Suponiendo columnas ['SKU','PriceList'] en tu CSV de precios
    raw = raw.merge(price_df, on='SKU', how='left')

    # 3) Agregar
    agg = aggregate(raw)

    # 4) Leer input de comerciales
    input_df = pd.read_csv('data/forecast_input.csv', parse_dates=['Date'])

    # 5) Merge con input
    combined = merge_with_input(agg, input_df)

    # 6) Forecast automático
    periods = cfg['forecast']['periods']
    fc = apply_forecast(combined, periods)

    # 7) Guardar outputs
    combined.to_csv('outputs/consolidated.csv', index=False)
    fc.to_csv('outputs/auto_forecast.csv', index=False)

if __name__ == "__main__":
    main()

