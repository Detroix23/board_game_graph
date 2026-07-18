"""
# Board game graphing: utilities.
/src/board_games_maths/debug.py
"""
import numpy

from typing import Union, NoReturn

def assert_eq(a: object, b: object) -> Union[bool, NoReturn]:
    """
    Compare `a` and `b`:
    - if `a == b`: return `True`;
    - else: raise a ***verbose*** `AssertionError`.
    """
    end: Union[bool, Exception] = True

    try:
        if isinstance(a, numpy.ndarray) and isinstance(b, numpy.ndarray):
            assert (a == b).all()
        else:
            assert a == b
            
    except AssertionError:
        end = AssertionError(f"""(X) assert_eq(a, b) *not equal*:
- `a` = `{a}`;
- `b` = `{b}`.               
""")

    except Exception as exception:
        print(f"""(X) assert_eq(a, b) *fail*:
- `a` = `{a}`;
- `b` = `{b}`.               
""")
        end = exception

    if isinstance(end, Exception):
        raise end 

    return True

def assert_neq(a: object, b: object) -> Union[bool, NoReturn]:
    """
    Compare `a` and `b`:
    - if `a != b`: return `True`;
    - else: raise a ***verbose*** `AssertionError`.
    """
    end: Union[bool, Exception] = True

    try:
        if isinstance(a, numpy.ndarray) and isinstance(b, numpy.ndarray):
            assert (a != b).all()
        else:
            assert a != b
            
    except AssertionError:
        end = AssertionError(f"""(X) assert_eq(a, b) *equal*:
- `a` = `{a}`;
- `b` = `{b}`.               
""")

    except Exception as exception:
        print(f"""(X) assert_eq(a, b) *fail*:
- `a` = `{a}`;
- `b` = `{b}`.               
""")
        end = exception

    if isinstance(end, Exception):
        raise end 

    return True

def debug_print(
    message: str,
    enable: bool = False, 
    *,
    end: str = "\n",
    flush: bool = False
) -> None:
    if enable:
        print(message, end=end, flush=flush)
    return
