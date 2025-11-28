import pandas as pd
import requests
import io

url = "https://opendata.schleswig-holstein.de/dataset/88ffe2cd-da5f-4ca7-960f-8049dd6f0de8/resource/1485a82e-f378-4372-82ba-a8fc62229572/download/opendata_wka_ib_gv_vb_sh_20251020.csv"

try:
    response = requests.get(url)
    response.raise_for_status()
    # Try reading with default separator first, then semicolon if needed
    try:
        df = pd.read_csv(io.StringIO(response.text), nrows=5)
    except:
        df = pd.read_csv(io.StringIO(response.text), sep=';', nrows=5)
    
    print("Columns:")
    print(df.columns.tolist())
    print("\nFirst 2 rows:")
    print(df.head(2))
except Exception as e:
    print(f"Error: {e}")
