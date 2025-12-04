# AI Task Planning Template

## 1. Task Title
Create a Visually Appealing Streamlit Frontend for Table RAG System

## 2. Task Overview
Develop an interactive Streamlit web application that provides a user-friendly interface for the existing Table RAG system. The frontend will allow users to query the coffee sales database using natural language, visualize the generated SQL queries, display query results, and present AI-generated answers in an intuitive and visually appealing manner.

## 3. Project Analysis

### Project Context
- **Current State:** The Table RAG system exists as a Python script (`table_rag.py`) with core functionality implemented. The system uses LangChain with Groq (Llama 3.3 70B) to generate SQL queries from natural language questions and answer them using RAG. The backend logic is complete but lacks a user interface.
- **Relevant Codebase:** 
  - `scripts/M07_VectorDB_RAG/table_rag/table_rag.py` - Main RAG implementation with functions: `fetch_information_from_db()`, `create_sql_query()`, and `rag()`
  - `scripts/M07_VectorDB_RAG/table_rag/data_prep.py` - Database creation script
  - SQLite database: `coffee_sales.db` with coffee sales data schema

### Dependencies & Constraints
- **Required Libraries/APIs:** 
  - Streamlit (for frontend framework)
  - Existing dependencies: `langchain_groq`, `langchain_core`, `pydantic`, `sqlite3`, `python-dotenv`
  - Streamlit visualization libraries: `plotly` or `streamlit-plotly` for interactive charts (optional)
- **Constraints:** 
  - Must maintain compatibility with existing backend functions
  - Database file (`coffee_sales.db`) must be accessible
  - Environment variables (Groq API key) must be properly configured
  - Should handle errors gracefully (SQL errors, API failures, etc.)

## 4. Context & Problem Definition
- **Background:** The Table RAG system demonstrates how to use LLMs to generate SQL queries and answer questions about structured data. Currently, users must modify the Python script directly to ask questions, which is not user-friendly. A Streamlit frontend will make this system accessible to non-technical users and provide a better demonstration of the RAG capabilities.
- **The Problem:** Create an intuitive web interface that:
  1. Accepts natural language queries from users
  2. Displays the generated SQL query transparently
  3. Shows the raw database results
  4. Presents the AI-generated answer in a readable format
  5. Provides visual feedback during processing
  6. Handles errors gracefully with user-friendly messages
  7. Includes optional data visualization for query results

## 5. Technical Requirements
- **Platform/Environment:** 
  - Python 3.8+ (compatible with existing dependencies)
  - Streamlit 1.28.0+
  - Existing environment setup with `.env` file for API keys
- **Key Functionality:** 
  1. Text input for user queries
  2. Query execution with loading indicators
  3. Display of generated SQL query (with syntax highlighting if possible)
  4. Display of raw database results in a table format
  5. Display of AI-generated natural language answer
  6. Error handling and user feedback
  7. Optional: Query history/session management
  8. Optional: Basic data visualization (charts for numeric results)
- **Performance:** 
  - Should respond within reasonable time (depends on Groq API latency)
  - Display loading states during API calls
  - Cache table schema information if possible
- **Security:** 
  - Ensure database queries are read-only (SELECT only)
  - Validate user input to prevent SQL injection (though LLM-generated queries should be safe)
  - Keep API keys secure (already handled via .env)

## 6. API & Backend Changes
### New Endpoints
*No new API endpoints required - Streamlit will call existing Python functions directly.*

### Database Schema Changes
*No database schema changes required.*

### Logic/Business Rules
- Add input validation for user queries (non-empty, reasonable length)
- Implement SQL query validation to ensure only SELECT statements are executed
- Add error handling wrapper functions for better user experience
- Consider adding query result caching for repeated queries (optional)

## 7. Frontend Changes
- **UI Components:** 
  1. **Header/Title Section:** App title, description, and branding
  2. **Query Input Section:** Text area or input field for natural language queries
  3. **Action Button:** "Ask Question" or "Query Database" button
  4. **Loading Indicator:** Spinner or progress bar during processing
  5. **SQL Query Display:** Code block showing generated SQL (with syntax highlighting)
  6. **Results Table:** Streamlit dataframe display for database results
  7. **Answer Section:** Formatted text area showing AI-generated answer
  8. **Error Display:** Alert/error message component for failures
  9. **Optional:** Sidebar with app info, query history, or settings
  10. **Optional:** Visualization section for numeric results (charts, graphs)

- **User Flow:** 
  1. User opens the Streamlit app
  2. User sees welcome message and instructions
  3. User enters a natural language question in the input field
  4. User clicks "Ask Question" button
  5. Loading indicator appears
  6. System generates SQL query (displayed to user)
  7. System executes query and retrieves results (displayed in table)
  8. System generates natural language answer (displayed prominently)
  9. User can ask follow-up questions or modify query

- **State Management:** 
  - Use Streamlit's session state for:
    - Query history (optional)
    - Previous results (optional)
    - User preferences (optional)
  - Streamlit's reactive execution model will handle most state automatically

## 8. Implementation Plan
### Step 1: Planning & Design
1. Sketch UI layout (header, input section, results sections)
2. Design component hierarchy and organization
3. Plan error handling strategy
4. Decide on optional features (visualization, history)
5. Create mockup or wireframe of desired UI

### Step 2: Backend Implementation
1. Create wrapper functions for error handling around existing RAG functions
2. Add input validation functions
3. Add SQL query validation (ensure SELECT-only)
4. Create utility functions for formatting results
5. Add optional caching mechanism for table schema

### Step 3: Frontend Implementation
1. Set up Streamlit app structure (`streamlit_app.py` or `app.py`)
2. Create header section with title and description
3. Implement query input component with text area
4. Add submit button with proper styling
5. Implement loading state handling
6. Create SQL query display section (use `st.code()` with syntax highlighting)
7. Create results table display (use `st.dataframe()`)
8. Create answer display section with formatted text
9. Implement error handling UI (use `st.error()`)
10. Add optional sidebar with app information
11. Style components for visual appeal (colors, spacing, icons)
12. Add optional visualization components for numeric results

### Step 4: Integration & Testing
1. Test end-to-end flow with various query types
2. Test error scenarios (invalid queries, API failures, database errors)
3. Verify UI responsiveness and loading states
4. Test with different screen sizes (Streamlit responsive design)
5. Validate that all existing functionality works through the UI
6. Add user instructions/help text
7. Polish visual design and spacing

## 9. File Structure & Organization
### New Files
- `scripts/M07_VectorDB_RAG/table_rag/streamlit_app.py` - Main Streamlit application file
- `scripts/M07_VectorDB_RAG/table_rag/utils.py` - Optional utility functions for formatting, validation (if needed)
- `scripts/M07_VectorDB_RAG/table_rag/requirements.txt` - Updated with Streamlit dependency (if not already present)

### Modified Files
- Potentially refactor `table_rag.py` to separate UI logic from core RAG logic (optional, for better organization)

### File Organization
```
scripts/M07_VectorDB_RAG/table_rag/
├── table_rag.py          # Existing RAG backend (keep as is)
├── data_prep.py          # Existing data preparation (keep as is)
├── streamlit_app.py       # New Streamlit frontend
├── utils.py               # Optional utility functions
├── coffee_sales.db        # Database file
└── requirements.txt       # Dependencies
```

