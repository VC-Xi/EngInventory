"""
D8: Mergesort (stable). Used for report exports.

best, average, worst time: O(n log n)
space: O(n)
"""

from typing import Any, Callable, List, Optional


def merge_sort(items: List[Any], key_func: Optional[Callable] = None) -> List[Any]:
    """Return a new sorted list. O(n log n)."""
    if len(items) <= 1:
        return list(items)
    if key_func is None:
        key_func = lambda value: value

    middle = len(items) // 2
    left = merge_sort(items[:middle], key_func)
    right = merge_sort(items[middle:], key_func)

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):  # <= keeps it stable
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]