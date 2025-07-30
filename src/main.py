import pandas as pd
from src.extract import extract_data
from src.transform import aggregate, merge_with_input
from src.forecast import apply_forecast
import yaml

def main():
    # 1) Extraer
    raw = extract_data()

    # 2) Agrupar
    agg = aggregate(raw)

    # 3) Leer input de comerciales
    input_df = pd.read_csv('data/forecast_input.csv', parse_dates=['Date'])

    # 4) Merge
    combined = merge_with_input(agg, input_df)

    # 5) Forecast automático
    cfg = yaml.safe_load(open('config/config.yaml'))['forecast']
    fc = apply_forecast(combined, cfg['periods'])

    # 6) Guardar outputs
    combined.to_csv('outputs/consolidated.csv', index=False)
    fc.to_csv('outputs/auto_forecast.csv', index=False)

if __name__ == "__main__":
    main()

