# AI Task Plan — Dash Snake (Nokia 3210 style)

## 1. Task Title
Dash-based, old-school Nokia 3210-style Snake game prototype

## 2. Task Overview
Build a lightweight Dash application that recreates the classic Snake game (Nokia 3210 feel): monochrome-ish UI, grid-based movement, soundless minimal UX, keyboard controls (arrows / WASD), and replayable sessions. The app will be educational: show game state, score, and internal timing. It will be easy to extend (difficulty modes, multiple board sizes, AI player) and include testable game logic separated from the UI.

## 3. Project Analysis

### Project Context
- **Current State:** This repository contains Python notebooks and scripts; there is no Dash game implemented. This task adds a new educational demo under `scripts_MSO/day 4/dash_snake`.
- **Relevant Codebase:** New files will sit alongside other `scripts_MSO` examples. Existing CI/tests won't be changed initially.

### Dependencies & Constraints
- **Required Libraries/APIs:** Python 3.10+ (the repo uses 3.12 in pyproject), Dash (dash, plotly), pandas/numpy only if needed for state handling, pytest for tests.
- **Constraints:** Keep the implementation single-file runnable prototype and keep UI simple (avoid heavy graphics). Keyboard input handling in Dash requires clientside JS callbacks; we will implement minimal JS to capture arrow and WASD presses.

## 4. Context & Problem Definition
- **Background:** The classic Snake is an approachable interactive example for game loops, input handling, and reactive web front-ends with Dash. It’s a great teaching demo for event-driven programming.
- **The Problem:** Implement a responsive, low-latency grid-based game loop in Dash, handle keyboard input reliably in the web environment, and separate game logic from presentation for tests.

## 5. Technical Requirements
- **Platform/Environment:** Python 3.12 (consistent with the repo), runs locally in a browser served by Dash.
- **Key Functionality:**
  - Grid-based Snake game (configurable grid sizes e.g., 11x11 Nokia sized classic)
  - Keyboard controls (arrow keys + WASD)
  - Start / Pause / Reset controls
  - Score display and high-score memory (in-memory for demo)
  - Visual board display (SVG or Plotly) with clean low-res look
  - Optional autoplay/AI demo mode (simple rule-based)
- **Performance:** Smooth updates at a configurable tick rate (e.g., 6–12 updates/sec), must handle up to ~500 ms latency tolerable in a simple demo.
- **Security:** No external network calls, no remote execution. Keep client-side JavaScript minimal and safe.

## 6. API & Backend Changes
### New Endpoints
No REST endpoints required — Dash callback-based UI only.

### Database Schema Changes
None. High score stored in-memory or local JSON file for demo persistence.

### Logic/Business Rules
- Snake moves one cell per tick in the chosen direction.
- Hitting the wall or the snake's body ends the game.
- Eating food grows the snake and increases score.
- Optional: wrap-around mode toggle to permit crossing edges.

## 7. Frontend Changes
- **UI Components:**
  - Game canvas rendering grid and snake (Plotly scatter or SVG)
  - Start / Pause / Reset Buttons
  - Speed slider / difficulty selector
  - Toggle: wrap-around vs walls
  - Score display and small game stats (steps, snake length)
  - Keyboard capture layer (client-side JS) integrated via Dash clientside callbacks
- **User Flow:**
  1. User opens the Dash app in a browser.
  2. Clicks Start — keyboard controls enabled.
  3. User plays, score updates live; pause / reset working.
  4. User can toggle difficulty or try autoplay to observe behavior.
- **State Management:**
  - Store game state on the server in a `dcc.Store` component serialized as a small JSON structure: snake body coordinates, direction, food coordinate, running/paused flag, score. Dash callbacks update the state at each tick.

## 8. Implementation Plan
### Step 1: Planning & Design
1. Choose a simple representation for game state: list of (x,y) cells for the snake, a tuple for food, integer score, and metadata.
2. Decide on rendering technology: Plotly scatter with square markers or inline SVG generation via HTML + CSS. Plotly has clearer cross-browser support inside Dash.

### Step 2: Backend Implementation (Game logic)
1. Create `game_engine.py` with pure-Python functions:
   - new_game(grid_size)
   - step_game(state, direction) -> new_state, event (e.g. 'ate', 'dead', 'moved')
   - change_direction(state, new_dir)
2. Add unit tests for all rules (growth, collision, wrap-around)

### Step 3: Frontend Implementation (Dash UI)
1. Create `dash_snake.py` as the app entrypoint.
2. Implement board rendering callback from `dcc.Interval` ticks and state store.
3. Implement clientside JS code to capture keypresses and send them to Dash as events (small script added to assets or component's `dangerously_allow_js` depending on Dash version).
4. Add controls, score board, and settings.

### Step 4: Integration & Testing
1. Add end-to-end tests using `dash.testing` to simulate keyboard events and assert game progression.
2. Add unit tests for `game_engine` and small integration tests for state transitions.

## 9. File Structure & Organization
### New Files
- `scripts_MSO/day 4/dash_snake/`
  - `game_engine.py` (pure logic, testable)
  - `dash_snake.py` (Dash app entrypoint)
  - `assets/keyboard.js` (small client-side key capture script)
  - `tests/test_game_engine.py` (unit tests for engine)
  - `tests/test_dash_app_e2e.py` (e2e tests using dash.testing)
  - `README.md` (how to run the demo and tests)

## 10. Acceptance Criteria
- Reproducible game rules that match classic Snake behaviour (growth, death conditions).
- Working Dash app that responds to keyboard controls and can start/pause/reset.
- Tests sufficient to validate engine correctness and a basic end-to-end flow.

## 11. Risks & Mitigations
- Risk: Capturing keyboard reliably in Dash can be tricky across browsers. Mitigation: add simple client-side JS capture and degrade gracefully to clickable buttons.
- Risk: Dash callbacks and frequent ticks may overload synchronous server. Mitigation: keep tick rate moderate (e.g., 8 Hz) and keep engine code lightweight.

## 12. Timeline & Milestones
- Day 1: Implement `game_engine.py` and unit tests.
- Day 2: Build Dash app UI, integrate keyboard capture, basic styling.
- Day 3: Add e2e tests, polish visuals, update README.

## 13. Next Steps / Immediate Action Items
1. Add the new folder and create `game_engine.py` and `dash_snake.py`.
2. Implement unit tests for the engine — get green test runs.
3. Implement Dash UI, including keyboard capture.
4. Add e2e integration tests and brief README for how to run the game.
