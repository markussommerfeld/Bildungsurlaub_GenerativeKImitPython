"""Simple AEP calculation and uncertainty propagation engine for the Dash demo.

This provides a deterministic AEP calculation from per-turbine annual energy
values and a small Monte Carlo wrapper that simulates uncertainties on key
parameters like multiplicative energy scale (wind speed / resource), availability,
and power curve shifts (simple scaling).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, Iterable, Tuple


def aep_from_production(df_production: pd.DataFrame) -> pd.DataFrame:
    """Compute deterministic AEP summary from a production DataFrame.

    Input DataFrame must contain ['turbine_id', 'annual_energy_mwh'].
    Returns DataFrame with per-turbine AEP (MWh) and park-level aggregation.
    """
    df = df_production.copy()
    if 'annual_energy_mwh' not in df.columns:
        raise ValueError('production DataFrame must include annual_energy_mwh')
    df['annual_energy_mwh'] = pd.to_numeric(df['annual_energy_mwh'], errors='coerce').fillna(0.0)
    total = df['annual_energy_mwh'].sum()
    return pd.DataFrame({
        'turbine_id': df['turbine_id'].astype(str),
        'annual_energy_mwh': df['annual_energy_mwh']
    }).assign(park_total_mwh=total)


def monte_carlo_aep(df_production: pd.DataFrame, n_samples: int = 1000,
                    energy_scale_std: float = 0.05,
                    availability_std: float = 0.01,
                    random_seed: int | None = None) -> Dict[str, np.ndarray]:
    """Monte Carlo propagation of simple multiplicative uncertainties.

    - energy_scale_std: multiplicative uncertainty (relative) applied to each
      turbine's annual energy (simulates wind resource uncertainty / power curve scale).
    - availability_std: uncertainty on availability (fractional). This is applied
      multiplicatively as well.

    Returns a dict with keys: 'samples' (park total samples), 'per_turbine' (dict
    mapping turbine_id -> samples array), 'percentiles' (DataFrame of percentiles)
    """
    rng = np.random.default_rng(random_seed)

    df = df_production.copy()
    ids = df['turbine_id'].astype(str).tolist()
    base = df['annual_energy_mwh'].to_numpy(dtype=float)

    # Sample multiplicative factors per sample and per turbine
    # energy scale: per-sample per-turbine lognormal-like using normal multiplier
    energy_factors = rng.normal(loc=1.0, scale=energy_scale_std, size=(n_samples, len(base)))
    availability_factors = rng.normal(loc=1.0, scale=availability_std, size=(n_samples, len(base)))

    # ensure no negative factors
    energy_factors = np.clip(energy_factors, 0.0, None)
    availability_factors = np.clip(availability_factors, 0.0, None)

    samples = (base * energy_factors * availability_factors).sum(axis=1)

    per_turbine = {}
    for i, tid in enumerate(ids):
        per_turbine[tid] = (base[i] * energy_factors[:, i] * availability_factors[:, i])

    # percentiles table for the park-level
    pcts = np.percentile(samples, [2.5, 16, 50, 84, 97.5])
    percentiles = pd.DataFrame({'percentile': ['2.5', '16', '50', '84', '97.5'], 'mwh': pcts})

    return {
        'samples': samples,
        'per_turbine': per_turbine,
        'percentiles': percentiles
    }


def summarize_montecarlo(result: Dict[str, np.ndarray]) -> pd.DataFrame:
    """Return a summary DataFrame (median, low, high) for park-level Monte Carlo.
    """
    p = result['percentiles']
    # return a small summary
    median = float(p.loc[p['percentile'] == '50', 'mwh'])
    lo = float(p.loc[p['percentile'] == '16', 'mwh'])
    hi = float(p.loc[p['percentile'] == '84', 'mwh'])
    return pd.DataFrame([{'metric': 'park_total_mwh', 'median': median, 'lo_1sigma': lo, 'hi_1sigma': hi}])
