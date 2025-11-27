import importlib.util
from pathlib import Path


def _load_game_engine(module_name='game_engine'):
    p = Path(__file__).resolve().parent.parent / 'game_engine.py'
    spec = importlib.util.spec_from_file_location(module_name, str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_new_game_basic():
    mod = _load_game_engine()
    new_game = mod.new_game
    step_game = mod.step_game
    change_direction = mod.change_direction

    st = new_game((7, 7), init_length=3, wrap=False, seed=42)
    assert st['grid'] == (7, 7)
    assert len(st['snake']) == 3
    assert st['direction'] == 'RIGHT'
    assert st['food'] is not None
    st = new_game((7, 7), init_length=3, wrap=False, seed=42)
    assert st['grid'] == (7, 7)
    assert len(st['snake']) == 3
    assert st['direction'] == 'RIGHT'
    assert st['food'] is not None


def test_step_move_forward():
    mod = _load_game_engine()
    new_game = mod.new_game
    step_game = mod.step_game

    st = new_game((5, 5), init_length=3, seed=0)
    st['running'] = True
    head_before = st['snake'][0]
    st2, ev = step_game(st)
    assert ev in ('moved', 'ate')
    # head should have changed
    assert st2['snake'][0] != head_before


def test_eat_food_and_grow():
    mod = _load_game_engine()
    new_game = mod.new_game
    step_game = mod.step_game

    st = new_game((5, 5), init_length=2, seed=1)
    # place food directly in front
    st['snake'] = [(2, 2), (1, 2)]
    st['direction'] = 'RIGHT'
    st['food'] = (3, 2)
    st['running'] = True
    before_len = len(st['snake'])
    st2, ev = step_game(st)
    assert ev == 'ate'
    assert len(st2['snake']) == before_len + 1
    assert st2['score'] == st['score'] + 1


def test_self_collision():
    mod = _load_game_engine()
    new_game = mod.new_game
    step_game = mod.step_game

    # make a small U shape so next step collides with body
    st = new_game((5, 5), init_length=4)
    st['snake'] = [(2, 2), (2, 3), (1, 3), (1, 2)]
    st['direction'] = 'UP'
    st['running'] = True
    st2, ev = step_game(st)
    assert ev == 'dead'


def test_wrap_around():
    mod = _load_game_engine()
    new_game = mod.new_game
    step_game = mod.step_game

    st = new_game((3, 3), init_length=2, wrap=True)
    # place head at edge and move right
    st['snake'] = [(2, 1), (1, 1)]
    st['direction'] = 'RIGHT'
    st['running'] = True
    st2, ev = step_game(st)
    # wrapped head should be at x=0
    assert st2['snake'][0][0] == 0
