from typing import Dict, Optional, Any

MM_PER_CM = 10.0
# we support at most 0.01nm
EPS = 1e-12


def to_mm_str(val_cm: float) -> str:
    """Convert a value in cm to mm and return it as a string"""
    mm = val_cm * MM_PER_CM
    if abs(mm - int(mm)) < EPS:
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
    """Convert a string from snake_case to PascalCase"""
    return "".join(part.capitalize() for part in s.split("_"))


def choose_solid_name(node: dict, counters: Dict[str, Dict[str, int]]) -> str:
    """Generate a unique solid name for a node"""
    return unique_name(f"solid{to_pascal_case(node.get('name', 'Figure'))}", "solid", counters)


def choose_logic_name(node: dict, counters: Optional[Dict[str, Dict[str, int]]] = None) -> str:
    """Generate a unique logic name for a node"""
    if counters is None:
        return f"logic{to_pascal_case(node.get('name', 'Figure'))}"
    return unique_name(f"logic{to_pascal_case(node.get('name', 'Figure'))}", "logic", counters)


def choose_phys_name(child_node: dict, counters: Dict[str, Dict[str, int]]) -> str:
    """Generate a unique physical volume name for a node"""
    return unique_name(f"phys{to_pascal_case(child_node.get('name', 'Figure'))}", "phys", counters)


def get_detector_name(detector: Dict[str, Any]) -> str:
    """Return detector name or fallback with uuid from JSON."""
    if "name" in detector and detector["name"]:
        return detector["name"]
    return f"UnknownDetector_{detector.get('uuid', 'noUUID')}"
