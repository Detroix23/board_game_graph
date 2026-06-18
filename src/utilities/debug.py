"""
# Board game graphing: utilities.
/src/board_games_maths/debug.py
"""
from typing import Union, NoReturn

def assert_eq(a: object, b: object) -> Union[bool, NoReturn]:
    """
    Compare `a` and `b`:
    - if `a == b`: return `True`;
    - else: raise a ***verbose*** `AssertionError`.
    """
    if a != b:
        raise AssertionError(f"""(X) assert_eq(a, b) *fail*:
- `a` = `{a}`;
- `b` = `{b}`.               
""")
    
    return True
