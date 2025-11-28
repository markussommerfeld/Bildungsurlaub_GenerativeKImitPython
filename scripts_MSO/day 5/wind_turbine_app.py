import dash
from dash import dcc, html, dash_table, Input, Output, State, callback_context
import pandas as pd
import plotly.express as px
import requests
import io
import os
from pyproj import Transformer
from geopy.distance import geodesic

# --- Configuration ---
CSV_URL = "https://opendata.schleswig-holstein.de/dataset/88ffe2cd-da5f-4ca7-960f-8049dd6f0de8/resource/1485a82e-f378-4372-82ba-a8fc62229572/download/opendata_wka_ib_gv_vb_sh_20251020.csv"
LOCAL_FILENAME = "wind_turbines_sh.csv"

# --- Data Loading & Processing ---
def load_data():
    if os.path.exists(LOCAL_FILENAME):
        print("Loading data from local file...")
        df = pd.read_csv(LOCAL_FILENAME, sep=None, engine='python') # Auto-detect separator
    else:
        print("Downloading data...")
        try:
            response = requests.get(CSV_URL)
            response.raise_for_status()
            # Try to detect separator, default to comma, fallback to semicolon
            content = response.text
            try:
                df = pd.read_csv(io.StringIO(content))
            except:
                df = pd.read_csv(io.StringIO(content), sep=';')
            
            # Save to local file for caching
            df.to_csv(LOCAL_FILENAME, index=False)
        except Exception as e:
            print(f"Error downloading data: {e}")
            return pd.DataFrame()

    # Coordinate Conversion (UTM 32N to WGS84)
    # Assuming OSTWERT/NORDWERT are in EPSG:25832 (ETRS89 / UTM zone 32N)
    if 'OSTWERT' in df.columns and 'NORDWERT' in df.columns:
        transformer = Transformer.from_crs("EPSG:25832", "EPSG:4326", always_xy=True)
        
        # Handle non-numeric values if any
        df['OSTWERT'] = pd.to_numeric(df['OSTWERT'], errors='coerce')
        df['NORDWERT'] = pd.to_numeric(df['NORDWERT'], errors='coerce')
        df = df.dropna(subset=['OSTWERT', 'NORDWERT'])

        lon, lat = transformer.transform(df['OSTWERT'].values, df['NORDWERT'].values)
        df['Longitude'] = lon
        df['Latitude'] = lat
    
    return df

df = load_data()

# --- Dash App ---
app = dash.Dash(__name__, title="Wind Turbine Analysis SH")
server = app.server

app.layout = html.Div([
    html.H1("Wind Turbine Analysis - Schleswig-Holstein", style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.H3("Find Closest Turbine"),
            html.Label("Latitude:"),
            dcc.Input(id='input-lat', type='number', placeholder="e.g., 54.32", step=0.0001),
            html.Label("Longitude:"),
            dcc.Input(id='input-lon', type='number', placeholder="e.g., 10.12", step=0.0001),
            html.Button('Search', id='btn-search', n_clicks=0),
            html.Div(id='search-output', style={'marginTop': '10px', 'whiteSpace': 'pre-wrap'})
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px', 'backgroundColor': '#f9f9f9'}),
        
        html.Div([
            dcc.Graph(id='map-graph')
        ], style={'width': '65%', 'display': 'inline-block'})
    ]),

    html.Hr(),
    
    html.H3("Data Table"),
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_size=10,
        style_table={'overflowX': 'auto'},
    )
])

@app.callback(
    [Output('map-graph', 'figure'),
     Output('search-output', 'children')],
    [Input('btn-search', 'n_clicks'),
     Input('data-table', 'derived_virtual_data')],
    [State('input-lat', 'value'),
     State('input-lon', 'value')]
)
def update_map_and_search(n_clicks, rows, search_lat, search_lon):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    # Use filtered data from table if available, else original df
    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)

    if dff.empty:
        return px.scatter_mapbox(lat=[], lon=[], zoom=7), "No data available."

    # Default map
    fig = px.scatter_mapbox(
        dff, 
        lat="Latitude", 
        lon="Longitude", 
        hover_name="HERSTELLER",
        hover_data=["GEMEINDE", "LEISTUNG", "NABENHOEHE"],
        zoom=7, 
        height=600
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    search_result = ""

    # Handle Search
    if triggered_id == 'btn-search' and search_lat is not None and search_lon is not None:
        user_coords = (search_lat, search_lon)
        
        # Calculate distances
        # We need to iterate or use apply. For performance on larger datasets, cKDTree is better, 
        # but for ~3000 rows, apply is fine.
        def calc_dist(row):
            return geodesic(user_coords, (row['Latitude'], row['Longitude'])).km
        
        # Calculate distance for ALL rows in the original dataframe to find the absolute closest
        # Or just the filtered ones? Usually closest in the whole dataset makes more sense unless specified.
        # Let's search in the currently filtered data to be consistent with the view.
        
        if not dff.empty:
            dff['distance_km'] = dff.apply(calc_dist, axis=1)
            closest_turbine = dff.loc[dff['distance_km'].idxmin()]
            
            dist = closest_turbine['distance_km']
            name = closest_turbine.get('HERSTELLER', 'Unknown')
            loc = closest_turbine.get('GEMEINDE', 'Unknown')
            
            search_result = f"Closest Turbine:\nManufacturer: {name}\nLocation: {loc}\nDistance: {dist:.2f} km"
            
            # Highlight on map
            # Add a special trace for the user location and the closest turbine
            
            # User location
            fig.add_scattermapbox(
                lat=[search_lat],
                lon=[search_lon],
                mode='markers',
                marker=dict(size=15, color='red'),
                name='You'
            )
            
            # Closest turbine highlight
            fig.add_scattermapbox(
                lat=[closest_turbine['Latitude']],
                lon=[closest_turbine['Longitude']],
                mode='markers',
                marker=dict(size=15, color='green'),
                name='Closest Turbine'
            )
            
            # Center map
            fig.update_layout(
                mapbox=dict(
                    center=dict(lat=search_lat, lon=search_lon),
                    zoom=10
                )
            )

    return fig, search_result

if __name__ == '__main__':
    app.run(debug=True)
