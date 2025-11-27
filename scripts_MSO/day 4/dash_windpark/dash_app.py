"""Minimal Dash app scaffold for Windpark AEP & uncertainty visualisation.

This is intentionally a minimal, dependency-light server entrypoint. It uses
Dash if installed. The app demonstrates how the parser and aep engine are tied
together; heavy-lifting like Monte Carlo sampling should be sent to background
tasks in the real deployment.
"""
from __future__ import annotations

import os
from pathlib import Path
try:
    import dash
    from dash import dcc, html, Input, Output, State
    import plotly.express as px
except Exception:  # pragma: no cover - optional optional dependency
    dash = None

from .windpro_io import parse_production_table, parse_layout_table
from .aep_calc import aep_from_production, monte_carlo_aep
import pandas as pd


def create_app() -> 'dash.Dash | None':
    if dash is None:
        print('Dash is not installed in this environment. Install dash to run the demo app.')
        return None

    app = dash.Dash(__name__)

    sample_data_dir = Path(__file__).parent / 'example_data'
    sample_prod = sample_data_dir / 'windpro_production_sample.csv'

    # Load sample production data if available
    if sample_prod.exists():
        df_sample = pd.read_csv(sample_prod)
    else:
        # create a small sample
        df_sample = pd.DataFrame({'turbine_id': ['T1', 'T2', 'T3'], 'annual_energy_mwh': [3000, 3100, 2900]})

    summary_df = aep_from_production(df_sample)

    app.layout = html.Div([
        html.H2('Windpark AEP & Uncertainty — demo'),
        html.Div('Upload WindPRO production table or use sample'),
        dcc.Upload(id='upload', children=html.Button('Upload file')),
        html.Button('Run Monte Carlo (1000)', id='run_mc'),
        dcc.Loading(id='loading', children=html.Div(id='output_area')),
        dcc.Graph(id='aep_map'),
        dcc.Store(id='parsed_production', data=df_sample.to_dict(orient='records'))
    ])

    @app.callback(Output('output_area', 'children'), Input('run_mc', 'n_clicks'), State('parsed_production', 'data'))
    def on_run_mc(n_clicks: int, prod_data):
        if not n_clicks:
            return html.Pre(str(summary_df.head()))
        df = pd.DataFrame(prod_data)
        mc = monte_carlo_aep(df, n_samples=1000, random_seed=42)
        pct = mc['percentiles']
        return html.Pre(pct.to_string(index=False))

    @app.callback(Output('aep_map', 'figure'), Input('parsed_production', 'data'))
    def render_map(prod_data):
        df = pd.DataFrame(prod_data)
        # no position info in production sample — create fake grid for demo
        if 'x' not in df.columns or 'y' not in df.columns:
            coords = [(i * 500, i * 500) for i in range(len(df))]
            df['x'] = [c[0] for c in coords]
            df['y'] = [c[1] for c in coords]

        fig = px.scatter(df, x='x', y='y', text='turbine_id', size='annual_energy_mwh')
        fig.update_layout(title='Windpark turbine positions (demo)')
        return fig

    return app


if __name__ == '__main__':
    app = create_app()
    if app is not None:
        app.run_server(debug=True, port=int(os.environ.get('DASH_PORT', 8050)))
