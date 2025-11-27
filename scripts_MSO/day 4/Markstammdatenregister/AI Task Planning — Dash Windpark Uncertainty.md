# AI Task Plan — Dash interface for wind park uncertainty & AEP

## 1. Task Title
Dash app to compute uncertainties and Annual Energy Production (AEP) for wind turbines from WindPRO outputs and show park location on a map

## 2. Task Overview
Create an interactive Dash web app that:
- Ingests WindPRO exported Excel tables (production, wind resource, layout) in the background
- Computes AEP and uncertainty estimates (per-turbine and park-level)
- Displays numerical results, sensitivity/uncertainty breakdown, and interactive map of the wind park
- Allows user input to override or refine parameters and re-run calculations quickly

Expected outcome: A working prototype in the repo that can read sample WindPRO Excel files, compute AEP and uncertainty ranges, visualize results and the park map, and expose a simple programmatic API for downstream automation or CLI usage.

## 3. Project Analysis

### Project Context
- Current State: Existing repo with analysis scripts for RAG and vector DB; no Dash UI yet.
- Relevant Codebase: scripts_MSO folder contains experimental Python scripts. New UI will integrate with existing data-processing utilities or add new modules.

### Dependencies & Constraints
- Required Libraries/APIs:
  - Dash / Plotly
  - pandas, numpy
  - geopandas or folium (map rendering)
  - openpyxl / xlrd for Excel reading
  - shapely for geometric ops
  - optionally pyproj for reprojection
- Constraints:
  - Must support Excel formats exported from WindPRO (structure varies by version)
  - Must run on Windows dev environment; keep dependency versions compatible
  - Privacy: no external data upload to third-party services (map rendering offline preferred)

## 4. Context & Problem Definition
- Background: WindPRO generates tabular outputs describing turbine yields, wind roses and layout; engineers need quick visualization and uncertainty quantification without re-running full software.
- The Problem: Create a lightweight, reproducible interface to read WindPRO tables, compute AEP with uncertainty propagation (measurement and parameter uncertainties), visualize results and location, and allow fast scenario testing.

## 5. Technical Requirements
- Platform: Python 3.10+ on Windows
- Core functionality:
  - File import: accept WindPRO Excel exports and parse expected sheets
  - AEP computation: sum per-turbine energy, apply availability and losses
  - Uncertainty model: propagate wind speed variability, measurement error, power curve uncertainties to give AEP confidence intervals
  - Map display: show turbine locations, optional basemap, interactive details per turbine
  - UI: numeric inputs, file upload, scenario parameters, results panels
- Performance: handle parks up to ~200 turbines interactively; background tasks should not block UI
- Security: local-only by default, no external network calls required for processing

## 6. API & Backend Changes

### New Endpoints
- None required if using pure Dash app. If a REST API is desired:
  - POST /api/compute — accept parsed data or Excel file, return results and diagnostics
  - GET /api/park/{id}/map — return GeoJSON or tiles for map rendering

### Database Schema Changes
- Not required. Use in-memory for prototype. Optionally add SQLite/JSON store for saved scenarios.

### Logic/Business Rules
- Parsing rules for WindPRO Excel: robust handling of missing columns and minor format variations
- AEP = integral over wind speed distribution * turbine power curve * losses * availability
- Uncertainty propagation: ensemble Monte Carlo by sampling wind speed distribution and uncertain parameters, or analytic approximations when appropriate
- Input validation and clear error messages for ambiguous Excel layouts

## 7. Frontend Changes
- UI Components:
  - File upload/select component
  - Parameter entry panels: wind shear, air density correction, availability, losses
  - Compute button with progress indicator
  - Map panel (Plotly mapbox/folium or geopandas/geojson)
  - Results: table of per-turbine AEP + uncertainty, park summary, charts (CDF, histogram, sensitivity)
  - Export results button (CSV/Excel)
- User Flow:
  1. Upload WindPRO Excel (or pick sample)
  2. Inspect parsed sheets/turbine list
  3. Adjust parameters / select uncertainty model
  4. Run compute
  5. Explore map and result tables, export or save scenario
- State Management:
  - Dash server-side callbacks and store component for parsed data and computed results
  - Keep heavy compute in a background worker (Celery, threading, or Dash callback with async pattern)

## 8. Implementation Plan

### Step 1: Planning & Design
- Gather a representative set of WindPRO Excel exports (production, layout, wind resource) as test fixtures.
- Define a minimal, well-documented Excel parsing spec: expected sheet names and column names with fallbacks.
- Define the uncertainty propagation approach (Monte Carlo sampling by default) and minimal computational API surface.

### Step 2: Backend Implementation
1. Create a parser module: windpro_io.py
   - Functions: parse_production_table, parse_layout_table, parse_windrose
   - Unit tests with test fixtures
2. Implement core AEP engine: aep_calc.py
   - Deterministic AEP calculation
   - Uncertainty engine: sample parameters (wind speed scale, power curve shift, availability) and compute CI
   - Tests: analytic cases and Monte Carlo stability checks
3. Add a small synchronous API (module functions) that returns JSON-friendly results for the UI

### Step 3: Frontend Implementation
1. Scaffold Dash app: dash_app.py
   - File upload and parsing status screens
   - Panels for parameter inputs and compute button
2. Add map visualization using Plotly mapbox or folium with GeoJSON export
3. Add plots: per-turbine AEP bar + CI, park-level CDF, sensitivity tornado chart

### Step 4: Integration & Testing
1. Wire backend functions to Dash callbacks
2. Implement background tasks for Monte Carlo (simple worker thread or async callback)
3. Add end-to-end tests using pytest + Dash testing utilities (dash.testing) or integration tests that run the app headlessly and assert results for test fixtures
4. Manual acceptance testing for multiple WindPRO example files

## 9. File Structure & Organization
### New Files
- scripts_MSO/day 4/dash_windpark/
  - windpro_io.py        # parse WindPRO Excel exports
  - aep_calc.py          # deterministic and uncertainty AEP calculations
  - dash_app.py          # Dash UI server and callbacks
  - assets/              # images and stylesheet for the Dash app
  - tests/
    - test_windpro_io.py
    - test_aep_calc.py
    - test_dash_app_e2e.py
  - example_data/
    - windpro_production_sample.xlsx
    - windpro_layout_sample.xlsx
    - windrose_sample.xlsx
  - README.md            # local instructions and sample commands

## 10. Tests & Validation
- Unit tests:
  - parser tests (multiple Excel variants)
  - deterministic AEP calculation with known small examples
  - uncertainty propagation returns consistent percentiles, reproducible with fixed seed
- Integration tests:
  - end-to-end Dash app tests with example datasets using dash.testing
- Acceptance tests:
  - sample Excel processed, map displayed, per-turbine AEP computed, CI reported, and export produced

## 11. Acceptance Criteria
- The app successfully loads provided WindPRO sample files and shows a parsed list of turbines.
- Deterministic AEP computation matches a baseline reference within tolerance.
- The uncertainty engine produces reproducible confidence intervals given a fixed RNG seed.
- Interactive map displays correct coordinates and per-turbine popups with AEP and CI.
- User can export computed results as CSV/Excel.
- Basic unit and integration tests pass in CI.

## 12. Risk & Mitigation
- Risk: WindPRO exports vary by version and region.
  - Mitigation: develop flexible parser with configuration mapping and include multiple sample fixtures.
- Risk: Monte Carlo takes too long for large parks.
  - Mitigation: expose sample count setting, use vectorized numpy operations, and add background worker and progress updates.
- Risk: Map visualization relies on external basemap/mobile constraints.
  - Mitigation: allow optional offline basemap and provide simple coordinate-only render.

## 13. Timeline & Milestones (Example)
- Day 1: Collect example files, parser scaffolding, and basic unit tests
- Day 2: Implement AEP engine and uncertainty sampling; tests for core logic
- Day 3: Build Dash UI prototype with map and parameter controls
- Day 4: Integration, background processing, and CI tests
- Day 5: Polish, docs, and finalize acceptance tests

## 14. Next Steps / Immediate Action Items
- Confirm WindPRO sample files and typical data variants.
- Create the new project folder and add a minimal parser and example tests.
- Implement basic Dash scaffold so stakeholders can try uploading sample files.
