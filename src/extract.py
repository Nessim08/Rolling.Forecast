# src/extract.py

import io
import pandas as pd
import yaml
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential

def load_config():
    return yaml.safe_load(open('config/config.yaml'))

def extract_from_sharepoint():
    cfg = load_config()['sharepoint']
    ext = cfg['extract']

    # 1) Conectar a SharePoint / OneDrive con autenticación moderna
    ctx = ClientContext(cfg['site_url']).with_credentials(
        UserCredential(cfg['username'], cfg['password'])
    )

    # 2) Acceder a la carpeta configurada
    folder = ctx.web.get_folder_by_server_relative_url(cfg['folder_path'])
    files = folder.files
    ctx.load(files)
    ctx.execute_query()

    dfs = []
    for file in files:
        name = file.properties["Name"]
        if name.lower().endswith('.csv'):
            # 3) Descargar el contenido del archivo
            download = ctx.web.get_file_by_server_relative_url(
                file.properties["ServerRelativeUrl"]
            ).download()  # esto devuelve un RequestOptions
            ctx.execute_query()
            content = download.content  # bytes del CSV

            # 4) Leer en pandas
            df = pd.read_csv(io.BytesIO(content), parse_dates=['Fecha'])

            # 5) Renombrar columnas a los nombres internos
            df = df.rename(columns={
                'Mercado': 'Market',
                'Canal': 'Channel',
                'SKU Pareto': 'SKU',
                'Fecha': 'Date',
                'Sales': 'Sales',
                'Price': 'Price',
                'Scenario': 'Scenario'
            })

            # 6) Seleccionar sólo las columnas que configuras
            df = df[['Market', 'Channel', 'SKU', 'Date', 'Sales', 'Price', 'Scenario']]

            # 7) Filtrar escenarios
            df = df[df['Scenario'].isin(ext['scenarios'])]

            dfs.append(df)

    if not dfs:
        raise ValueError("No CSV encontrados en la carpeta de SharePoint/OneDrive")

    # 8) Concatenar y devolver
    return pd.concat(dfs, ignore_index=True)

# Alias para main.py
def extract_data():
    return extract_from_sharepoint()




