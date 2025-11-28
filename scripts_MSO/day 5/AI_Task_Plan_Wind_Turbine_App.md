# AI Task Planning Template: Wind Turbine Analysis Dash App

## 1. Task Title
Wind Turbine Analysis Dash App

## 2. Task Overview
Create a Dash desktop application that downloads wind turbine data from a CSV URL, visualizes the data on an interactive map, displays it in a searchable database (table), and allows users to find the closest turbine to a specific set of input coordinates.

## 3. Project Analysis

### Project Context
- **Current State:** New project/script creation.
- **Relevant Codebase:** Python scripts in `scripts_MSO\day 5`.

### Dependencies & Constraints
- **Required Libraries/APIs:** 
    - `dash` (for the web app framework)
    - `pandas` (for data manipulation)
    - `plotly` (for map visualization)
    - `requests` (for downloading the CSV)
    - `geopy` or `scipy.spatial` (for distance calculation)
- **Constraints:** The app should run locally.

## 4. Context & Problem Definition
- **Background:** The user wants to analyze wind turbine data for Schleswig-Holstein using a user-friendly interface.
- **The Problem:** Need a tool to automatically fetch the latest data, visualize it, and perform spatial queries (closest turbine) without manual data handling.

## 5. Technical Requirements
- **Platform/Environment:** Python.
- **Key Functionality:**
    - Download CSV from `https://opendata.schleswig-holstein.de/dataset/windkraftanlagen-2025-10-20`.
    - Interactive Map (Scattermapbox or Densitymapbox).
    - Searchable Data Table.
    - Input fields for Latitude and Longitude.
    - Logic to calculate and highlight the closest turbine.
- **Performance:** Should handle the dataset size (likely moderate) efficiently.

## 6. API & Backend Changes
### New Endpoints
N/A (Local Dash App)

### Database Schema Changes
N/A (In-memory DataFrame)

### Logic/Business Rules
- **Data Fetching:** Check if file exists or download fresh on startup (or via button).
- **Distance Calculation:** Use Haversine formula or Geodesic distance to find the nearest point.

## 7. Frontend Changes
- **UI Components:**
    - Header/Title.
    - "Download Data" button (optional, or auto-load).
    - Map Component (`dcc.Graph`).
    - Data Table Component (`dash_table.DataTable`).
    - Input fields for "Latitude" and "Longitude".
    - Output area for "Closest Turbine" details.
- **User Flow:** User opens app -> Data loads -> User sees map and table -> User enters coords -> App highlights closest turbine.
- **State Management:** Dash Callbacks.

## 8. Implementation Plan
### Step 1: Planning & Design
- Define layout structure.
- Identify CSV column names (requires inspecting the CSV).

### Step 2: Backend Implementation
- Write function to download and load CSV.
- Write function to calculate distances.

### Step 3: Frontend Implementation
- Create Dash layout.
- Implement Callbacks for updating map and table.
- Implement Callback for closest turbine search.

### Step 4: Integration & Testing
- Run app.
- Verify data download.
- Test search functionality.
- Test coordinate search.

## 9. File Structure & Organization
### New Files
- `wind_turbine_app.py`
