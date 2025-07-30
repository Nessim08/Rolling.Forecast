import io
import pandas as pd
import yaml
from shareplum import Office365
from shareplum import Site
from shareplum.site import Version
from sqlalchemy import create_engine

def load_config():
    return yaml.safe_load(open('config/config.yaml'))

def extract_from_sharepoint():
    cfg = load_config()['sharepoint']
    # Autenticar
    authcookie = Office365(cfg['site_url'],
                           username=cfg['username'],
                           password=cfg['password']).GetCookies()
    site = Site(cfg['site_url'], version=Version.v365, authcookie=authcookie)
    folder = site.Folder(cfg['folder_path'])
    
    dfs = []
    for file_info in folder.files:
        name = file_info['Name']
        if name.lower().endswith('.csv'):
            content = folder.get_file(name)
            df = pd.read_csv(io.BytesIO(content), parse_dates=['Date'])
            dfs.append(df)
    if not dfs:
        raise ValueError("No CSV encontrados en SharePoint")
    return pd.concat(dfs, ignore_index=True)

def extract_from_db():
    cfg = load_config()['db']
    engine = create_engine(cfg['connection_string'])
    query = """
      SELECT Market, Channel, SKU, Date, Sales, Price
      FROM ForecastData
      WHERE FiscalYear='FY25' OR ForecastPeriod IN ('RF09','RF10')
    """
    return pd.read_sql(query, engine)

def extract_data():
    # Si quieres mezclar SharePoint + BD, llama a ambos y concatena
    df_sp = extract_from_sharepoint()
    # df_db = extract_from_db()
    # return pd.concat([df_sp, df_db], ignore_index=True)
    return df_sp

