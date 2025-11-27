"""Pure-Python game engine for a grid-based Snake game.

State representation (dict):
  - grid: (width, height)
  - snake: list of (x,y) tuples, head at index 0
  - direction: one of ('UP','DOWN','LEFT','RIGHT')
  - food: (x,y)
  - score: int
  - running: bool
  - wrap: bool

Functions are pure / functional where convenient to make testing straightforward.
"""
from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import random

Coord = Tuple[int, int]
State = Dict[str, object]


OPPOSITE = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT'
}


def _in_bounds(x: int, y: int, grid: Tuple[int, int]) -> bool:
    w, h = grid
    return 0 <= x < w and 0 <= y < h


def new_game(grid: Tuple[int, int] = (11, 11), init_length: int = 3, wrap: bool = False, seed: Optional[int] = None) -> State:
    """Create a new game state.

    For determinism in tests, a `seed` int can be provided to control RNG.
    """
    rng = random.Random(seed)
    w, h = grid
    # place snake horizontally in middle moving right
    center_x = w // 2
    center_y = h // 2
    snake: List[Coord] = [(center_x - i, center_y) for i in range(init_length)]
    direction = 'RIGHT'

    def _rand_food():
        while True:
            fx = rng.randrange(w)
            fy = rng.randrange(h)
            if (fx, fy) not in snake:
                return (fx, fy)

    food = _rand_food()

    return {
        'grid': (w, h),
        'snake': snake,
        'direction': direction,
        'food': food,
        'score': 0,
        'running': False,
        'wrap': wrap
    }


def change_direction(state: State, new_dir: str) -> State:
    """Return new state with direction changed if not opposite.

    No mutation — returns a new dict where direction was updated when allowed.
    """
    if new_dir not in OPPOSITE:
        return state
    if OPPOSITE[new_dir] == state['direction']:
        # ignore opposite direction changes
        return state
    new_state = dict(state)
    new_state['direction'] = new_dir
    return new_state


def step_game(state: State, input_dir: Optional[str] = None) -> Tuple[State, str]:
    """Advance game one tick.

    Optionally provide input_dir to change direction this tick. Returns (new_state, event)
    where event is one of: 'moved', 'ate', 'dead', 'no_op' (if not running).
    """
    if not state.get('running', False):
        return state, 'no_op'

    s = dict(state)
    # shallow copies for lists
    snake: List[Coord] = [tuple(p) for p in state['snake']]
    grid = state['grid']
    w, h = grid

    if input_dir is not None and input_dir in OPPOSITE and OPPOSITE[input_dir] != state['direction']:
        direction = input_dir
    else:
        direction = state['direction']

    head_x, head_y = snake[0]
    if direction == 'UP':
        new_head = (head_x, head_y - 1)
    elif direction == 'DOWN':
        new_head = (head_x, head_y + 1)
    elif direction == 'LEFT':
        new_head = (head_x - 1, head_y)
    elif direction == 'RIGHT':
        new_head = (head_x + 1, head_y)
    else:
        new_head = (head_x, head_y)

    # handle wrap
    if state.get('wrap', False):
        nx = new_head[0] % w
        ny = new_head[1] % h
        new_head = (nx, ny)
    else:
        # check wall collision
        if not _in_bounds(new_head[0], new_head[1], grid):
            s['running'] = False
            return s, 'dead'

    # check self collision
    # note: tail will move unless we eat food; collision with tail that is moving off is allowed in that case
    # easiest approach: compute next snake body and check duplicates
    ate = new_head == tuple(state['food'])

    if ate:
        new_snake = [new_head] + snake
    else:
        new_snake = [new_head] + snake[:-1]

    if len(set(new_snake)) != len(new_snake):
        s['running'] = False
        s['snake'] = new_snake
        s['direction'] = direction
        return s, 'dead'

    # update state
    s['snake'] = new_snake
    s['direction'] = direction

    if ate:
        s['score'] = int(state['score']) + 1
        # place new food in free cell
        rng = random.Random()
        free_cells = [(x, y) for x in range(w) for y in range(h) if (x, y) not in new_snake]
        s['food'] = rng.choice(free_cells) if free_cells else None
        return s, 'ate'

    return s, 'moved'


if __name__ == '__main__':
    # quick manual demo
    st = new_game((11, 11), init_length=3, wrap=False, seed=1)
    st['running'] = True
    for i in range(5):
        st, ev = step_game(st)
        print(i, ev, st['snake'][0], 'score', st['score'])
