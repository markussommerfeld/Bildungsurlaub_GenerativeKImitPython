import pandas as pd
from dash_windpark.windpro_io import parse_production_table, parse_layout_table, parse_windrose


def test_parse_production_from_df():
    df = pd.DataFrame({'Turbine': ['T1', 'T2'], 'Annual energy (MWh)': [1000, 1500]})
    out = parse_production_table(df)
    assert 'turbine_id' in out.columns
    assert 'annual_energy_mwh' in out.columns
    assert out['annual_energy_mwh'].tolist() == [1000.0, 1500.0]


def test_parse_layout_basic():
    df = pd.DataFrame({'Turbine': ['T1', 'T2'], 'X': [100.0, 200.0], 'Y': [300.0, 400.0]})
    out = parse_layout_table(df)
    assert 'turbine_id' in out.columns
    assert 'x' in out.columns and 'y' in out.columns
    assert out['x'].tolist() == [100.0, 200.0]


def test_parse_windrose_values():
    df = pd.DataFrame({'Speed (m/s)': [5, 6, 7], 'Frequency (%)': [50, 30, 20]})
    out = parse_windrose(df)
    assert out is not None
    assert out['wind_speed'].tolist() == [5.0, 6.0, 7.0]
    assert pytest_approx_sum(out['frequency'].tolist())


def pytest_approx_sum(freqs, tol=1e-6):
    # helper for tests — expects frequencies normalized to 1.0 (or percentages that we normalize)
    s = sum(freqs)
    return abs(s - 1.0) < 1e-6 or abs(s - 100.0) < 1e-6
