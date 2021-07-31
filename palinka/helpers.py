from __future__ import annotations

from slugify import slugify

def c_id(name: str) -> str:
    """
        Return a C-friendly identifier
    """
    return slugify(name).replace('-', '_')

