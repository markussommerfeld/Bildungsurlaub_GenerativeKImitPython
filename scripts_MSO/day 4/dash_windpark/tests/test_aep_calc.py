import numpy as np
import pandas as pd
from dash_windpark.aep_calc import aep_from_production, monte_carlo_aep, summarize_montecarlo


def test_aep_from_production_basic():
    df = pd.DataFrame({'turbine_id': ['T1', 'T2'], 'annual_energy_mwh': [1000, 2000]})
    out = aep_from_production(df)
    assert 'park_total_mwh' in out.columns
    assert out['park_total_mwh'].iloc[0] == 3000


def test_monte_carlo_basic():
    df = pd.DataFrame({'turbine_id': ['T1', 'T2'], 'annual_energy_mwh': [1000, 2000]})
    res = monte_carlo_aep(df, n_samples=200, energy_scale_std=0.02, availability_std=0.005, random_seed=0)
    samples = res['samples']
    assert isinstance(samples, np.ndarray)
    assert samples.shape[0] == 200
    pct = res['percentiles']
    assert 'mwh' in pct.columns


def test_summarize_montecarlo():
    df = pd.DataFrame({'turbine_id': ['T1'], 'annual_energy_mwh': [1000]})
    res = monte_carlo_aep(df, n_samples=50, energy_scale_std=0.0, availability_std=0.0, random_seed=4)
    sum_df = summarize_montecarlo(res)
    assert sum_df['median'].iloc[0] == 1000.0
