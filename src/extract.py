import io
import pandas as pd
import yaml
from shareplum import Office365
from shareplum import Site
from shareplum.site import Version

def load_config():
    return yaml.safe_load(open('config/config.yaml'))

def extract_from_sharepoint():
    cfg = load_config()['sharepoint']
    ext = cfg['extract']

    # 1) Autenticación
    authcookie = Office365(
        cfg['site_url'],
        username=cfg['username'],
        password=cfg['password']
    ).GetCookies()
    site = Site(cfg['site_url'], version=Version.v365, authcookie=authcookie)
    folder = site.Folder(cfg['folder_path'])

    # 2) Leer y concatenar todos los CSV
    dfs = []
    for file_info in folder.files:
        name = file_info['Name']
        if name.lower().endswith('.csv'):
            content = folder.get_file(name)
            # parse_dates con el nombre original de la columna en tus CSV:
            df = pd.read_csv(io.BytesIO(content), parse_dates=['Fecha'])
            # Renombrar a los nombres que usa el downstream
            df = df.rename(columns={
                'Mercado': 'Market',
                'Canal': 'Channel',
                'SKU Pareto': 'SKU',
                'Fecha': 'Date',
                'Sales': 'Sales',
                'Price': 'Price',
                'Scenario': 'Scenario'
            })
            # 3) Selección de columnas
            df = df[['Market', 'Channel', 'SKU', 'Date', 'Sales', 'Price', 'Scenario']]
            # 4) Filtrar escenarios
            df = df[df['Scenario'].isin(ext['scenarios'])]
            dfs.append(df)

    if not dfs:
        raise ValueError("No CSV encontrados en SharePoint")

    return pd.concat(dfs, ignore_index=True)

# Alias para main.py
def extract_data():
    return extract_from_sharepoint()


