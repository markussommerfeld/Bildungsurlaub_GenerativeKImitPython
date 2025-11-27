"""Simple WindPRO Excel/CSV parser helpers for the Dash Windpark prototype.

This module provides lightweight parsers that accept either a pandas DataFrame
or a path to an Excel/CSV file and return canonical DataFrames used by the AEP
calculator (layout, production, windrose).

Designed to be small and robust for the demo; exact WindPRO formats should be
handled by adding more rules to the parsing functions when sample files are
available.
"""
from __future__ import annotations

from typing import Dict, Optional
import pandas as pd


def parse_production_table(source) -> pd.DataFrame:
    """Parse a production table from path or DataFrame into a canonical DataFrame.

    The returned DataFrame should include at least columns:
      - turbine_id (string)
      - annual_energy_mwh (float)  # per-turbine expected production

    Accepts either a path (str/Path) or an already-loaded DataFrame.
    """
    if isinstance(source, (str,)):
        if source.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(source)
        else:
            df = pd.read_csv(source)
    elif isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        raise TypeError("source must be a path or DataFrame")

    # Heuristics: common WindPRO production exports include columns named
    # like 'Turbine', 'Turbine ID', 'Annual energy (MWh)', 'Annual [MWh]'
    mapping = {}
    cols = [c.lower() for c in df.columns]
    if 'turbine' in cols:
        mapping[[c for c in df.columns if c.lower() == 'turbine'][0]] = 'turbine_id'
    elif 'turbine id' in cols:
        mapping[[c for c in df.columns if c.lower() == 'turbine id'][0]] = 'turbine_id'
    else:
        # fall back to first column
        mapping[df.columns[0]] = 'turbine_id'

    # find annual energy column
    ae_candidates = [c for c in df.columns if 'annual' in c.lower() and 'mwh' in c.lower()]
    if not ae_candidates:
        ae_candidates = [c for c in df.columns if 'annual' in c.lower()]
    if ae_candidates:
        mapping[ae_candidates[0]] = 'annual_energy_mwh'
    else:
        # try to detect 'production' columns
        prod_candidates = [c for c in df.columns if 'production' in c.lower() or 'yield' in c.lower()]
        if prod_candidates:
            mapping[prod_candidates[0]] = 'annual_energy_mwh'

    out = df.rename(columns=mapping)
    # ensure required columns exist
    if 'turbine_id' not in out.columns:
        out['turbine_id'] = out.index.astype(str)
    if 'annual_energy_mwh' not in out.columns:
        # default zeros
        out['annual_energy_mwh'] = 0.0

    # coerce types
    out['annual_energy_mwh'] = pd.to_numeric(out['annual_energy_mwh'], errors='coerce').fillna(0.0)
    out['turbine_id'] = out['turbine_id'].astype(str)

    return out[['turbine_id', 'annual_energy_mwh']]


def parse_layout_table(source) -> pd.DataFrame:
    """Parse layout table to return a DataFrame with turbine_id, x, y (or lat, lon).

    Returns canonical columns: ['turbine_id', 'x', 'y'] where coordinates may be
    local coordinates or lat/lon depending on the WindPRO export.
    """
    if isinstance(source, (str,)):
        if source.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(source)
        else:
            df = pd.read_csv(source)
    elif isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        raise TypeError("source must be a path or DataFrame")

    cols = [c.lower() for c in df.columns]
    # simple heuristics
    id_col = None
    for candidate in ('turbine', 'turbine id', 'id'):
        if candidate in cols:
            id_col = df.columns[cols.index(candidate)]
            break
    if id_col is None:
        id_col = df.columns[0]

    # find x/y or lat/lon
    x_col = None
    y_col = None
    for c in df.columns:
        nc = c.lower()
        if 'x' == nc or 'xcoord' in nc or 'x coordinate' in nc or 'easting' in nc:
            x_col = c
        if 'y' == nc or 'ycoord' in nc or 'y coordinate' in nc or 'northing' in nc:
            y_col = c
        if 'lat' in nc and x_col is None:
            x_col = c
        if 'lon' in nc and y_col is None:
            y_col = c

    if x_col is None or y_col is None:
        # fallback: try first two numeric columns
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if len(numeric_cols) >= 2:
            x_col, y_col = numeric_cols[:2]

    out = pd.DataFrame()
    out['turbine_id'] = df[id_col].astype(str)
    out['x'] = pd.to_numeric(df[x_col], errors='coerce') if x_col else 0.0
    out['y'] = pd.to_numeric(df[y_col], errors='coerce') if y_col else 0.0

    return out[['turbine_id', 'x', 'y']]


def parse_windrose(source) -> Optional[pd.DataFrame]:
    """Parse a windrose / wind resource sheet into a structured DataFrame.

    Returns a DataFrame with at least columns ['wind_speed','frequency'] or None if
    it cannot detect an appropriate sheet.
    """
    if isinstance(source, (str,)):
        if source.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(source)
        else:
            df = pd.read_csv(source)
    elif isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        raise TypeError("source must be a path or DataFrame")

    cols = [c.lower() for c in df.columns]
    speed_col = None
    freq_col = None
    for c in df.columns:
        nc = c.lower()
        if 'speed' in nc and speed_col is None:
            speed_col = c
        if any(k in nc for k in ('frequency', 'freq', '%')) and freq_col is None:
            freq_col = c

    if speed_col is None or freq_col is None:
        return None

    out = df[[speed_col, freq_col]].rename(columns={speed_col: 'wind_speed', freq_col: 'frequency'})
    out['wind_speed'] = pd.to_numeric(out['wind_speed'], errors='coerce')
    out['frequency'] = pd.to_numeric(out['frequency'], errors='coerce')
    out = out.dropna()
    # normalize frequencies to sum 1 if they are percentages
    if out['frequency'].sum() > 1.5:
        out['frequency'] = out['frequency'] / out['frequency'].sum()

    return out[['wind_speed', 'frequency']]
