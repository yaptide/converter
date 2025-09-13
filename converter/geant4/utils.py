from typing import Dict, Tuple, Optional, Set


_MM_PER_CM = 10.0
# we support at most 0.01nm
_EPS = 1e-12


def to_mm_str(val_cm: float) -> str:
    """Convert a value in cm to mm and return it as a string"""
    mm = val_cm * _MM_PER_CM
    if abs(mm - int(mm)) < _EPS:
        return str(int(mm))
    return f"{mm:g}"


def unique_name(base: str, kind: str, counters: Dict[str, Dict[str, int]]) -> str:
    """Generate a unique name for a given base string and category (solid, logic, phys)."""
    used = counters[kind]
    if base not in used:
        used[base] = 1
        return base
    used[base] += 1
    return f"{base}{used[base]}"

def to_pascal_case(s: str) -> str:
    """Convert a string with underscores to PascalCase from snake like case"""
    return "".join(part.capitalize() for part in s.split("_"))