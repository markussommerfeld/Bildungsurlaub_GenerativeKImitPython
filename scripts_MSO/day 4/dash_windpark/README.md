# Dash Windpark — AEP & Uncertainty prototype

This small demo shows a minimal structure for a Dash app that can read WindPRO-like
export tables, compute deterministic AEP and run a simple Monte Carlo uncertainty
propagation for park-level AEP, and visualize a map of turbine positions.

Quick start (developer machine):

1. Install required packages (recommended in a venv):

```powershell
python -m pip install -r requirements.txt
# or install minimal dev deps
python -m pip install pandas numpy dash plotly
```

2. Start the demo app:

```powershell
# Run the demo script directly (note the space in the path):
python "scripts_MSO/day 4/dash_windpark/dash_app.py"
```

3. Run tests (local dev machine)

```powershell
python -m pip install pytest
python -m pytest "scripts_MSO/day 4/dash_windpark/tests" -q
```

If `pytest` is not available in your environment (CI or local), install it in your virtualenv before running tests.

Notes
- The parser is intentionally permissive; add parsing rules for real WindPRO files.
- Monte Carlo implementation is simplistic and intended for demonstration.
