"""Dash app for playing a simple Snake game (Nokia 3210 feel) — lightweight demo.

This file is intentionally self-contained and uses the local `game_engine.py` via
importlib to avoid package import issues when running from the repo
directory (folder name contains a space on disk).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import json
import os

try:
    import dash
    from dash import dcc, html, Input, Output, State
    import plotly.graph_objs as go
except Exception:  # pragma: no cover - optional dependency
    dash = None


def _load_game_engine():
    p = Path(__file__).resolve().parent / 'game_engine.py'
    spec = importlib.util.spec_from_file_location('game_engine', str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def create_app():
    if dash is None:
        print('Dash not installed. Install dash to run the Snake demo.')
        return None

    mod = _load_game_engine()

    app = dash.Dash(__name__)

    initial_state = mod.new_game((11, 11), init_length=3, wrap=False, seed=2)
    initial_state['running'] = False

    app.layout = html.Div([
        html.H3('AI Snake — Nokia 3210 style demo'),
        html.Div(id='score', children='Score: 0'),
        html.Div([
            html.Button('Start', id='start', n_clicks=0),
            html.Button('Pause', id='pause', n_clicks=0),
            html.Button('Reset', id='reset', n_clicks=0),
            html.Label('Speed:'),
            dcc.Slider(id='speed', min=1, max=20, step=1, value=8),
        ], style={'display': 'flex', 'gap': '8px', 'alignItems': 'center'}),
        dcc.Input(id='key_input', type='text', value='', style={'display': 'none'}),
        dcc.Store(id='game_state', data=initial_state),
        dcc.Interval(id='tick', interval=200, n_intervals=0),
        dcc.Graph(id='game_board', style={'width': '420px', 'height': '420px'})
    ])

    @app.callback(Output('game_state', 'data'), [Input('tick', 'n_intervals'), Input('start', 'n_clicks'), Input('pause', 'n_clicks'), Input('reset', 'n_clicks'), Input('key_input', 'value')], State('game_state', 'data'), State('speed', 'value'))
    def tick(n_intervals, start_clicks, pause_clicks, reset_clicks, key_val, state, speed):
        # simple event prioritisation: reset > start/pause toggles > key
        if state is None:
            state = initial_state

        if reset_clicks:
            ns = mod.new_game(state['grid'], init_length=3, wrap=state.get('wrap', False))
            ns['running'] = False
            return ns

        # start/pause handling (start if start_clicks > pause_clicks)
        if start_clicks and start_clicks > pause_clicks:
            state['running'] = True
        if pause_clicks and pause_clicks >= start_clicks:
            state['running'] = False

        # handle keyboard
        if key_val:
            key = key_val.upper()
            mapping = {'ARROWLEFT': 'LEFT', 'LEFT': 'LEFT', 'A': 'LEFT',
                       'ARROWRIGHT': 'RIGHT', 'RIGHT': 'RIGHT', 'D': 'RIGHT',
                       'ARROWUP': 'UP', 'UP': 'UP', 'W': 'UP',
                       'ARROWDOWN': 'DOWN', 'DOWN': 'DOWN', 'S': 'DOWN'}
            new_dir = mapping.get(key)
            if new_dir:
                state = mod.change_direction(state, new_dir)

        # perform step on tick
        new_state, ev = mod.step_game(state)
        return new_state

    @app.callback(Output('game_board', 'figure'), Output('score', 'children'), Input('game_state', 'data'))
    def render(state):
        if state is None:
            return {}, 'Score: 0'

        w, h = state['grid']
        snake = state['snake']
        food = state.get('food')

        xs = [p[0] + 0.5 for p in snake]
        ys = [p[1] + 0.5 for p in snake]

        fig = go.Figure()
        # draw grid background
        fig.update_xaxes(range=[0, w], showgrid=True, dtick=1, zeroline=False, showticklabels=False)
        fig.update_yaxes(range=[0, h], showgrid=True, dtick=1, zeroline=False, showticklabels=False, scaleanchor='x')

        # snake body
        fig.add_trace(go.Scatter(x=xs, y=ys, mode='markers', marker=dict(size=40, color='black'), showlegend=False))

        # food
        if food:
            fig.add_trace(go.Scatter(x=[food[0] + 0.5], y=[food[1] + 0.5], mode='markers', marker=dict(size=20, color='red')))

        fig.update_layout(plot_bgcolor='white', margin=dict(l=10, r=10, t=30, b=10))
        score_text = f"Score: {state.get('score', 0)}"
        return fig, score_text

    return app


if __name__ == '__main__':
    app = create_app()
    if app:
        port = int(os.environ.get('DASH_PORT', 8051))
        app.run(debug=True, port=port)
