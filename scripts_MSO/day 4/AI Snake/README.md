# AI Snake — Nokia 3210 style demo

This folder contains a small Dash prototype that recreates a classic Snake game in a low-resolution, old-school style.

Quick start (developer machine):

1. Install dependencies (recommended into a virtual environment):

```powershell
python -m pip install dash plotly
```

2. Run the demo:

```powershell
python "scripts_MSO/day 4/AI Snake/dash_snake.py"
```

If Dash is not installed the script prints a message and exits.

Notes
- The core game logic lives in `game_engine.py` and is fully unit-tested in `tests/test_game_engine.py`.
- The app uses a small client-side `assets/keyboard.js` to populate the hidden input used for keyboard control events.
