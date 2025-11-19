"""TOON Format Encoder

Converts Python dictionaries to TOON format.
"""

from typing import Any, Dict, List, Union


def encode(data: Any, indent: int = 0) -> str:
    """
    Encode Python data structure to TOON format.
    
    Args:
        data: Python dict, list, or primitive to encode
        indent: Current indentation level (for recursion)
    
    Returns:
        TOON formatted string
    """
    if data is None:
        return 'null'
    
    if isinstance(data, bool):
        return 'true' if data else 'false'
    
    if isinstance(data, (int, float)):
        return str(data)
    
    if isinstance(data, str):
        # Quote strings that contain special characters
        if needs_quoting(data):
            return f'"{data}"'
        return data
    
    if isinstance(data, dict):
        return encode_dict(data, indent)
    
    if isinstance(data, list):
        return encode_array(data, indent)
    
    raise TypeError(f"Cannot encode type {type(data).__name__}")


def encode_dict(obj: Dict[str, Any], indent: int = 0) -> str:
    """
    Encode dictionary to TOON format with indentation.
    """
    lines = []
    indent_str = '  ' * indent
    
    for key, value in obj.items():
        if isinstance(value, dict):
            # Nested object
            lines.append(f"{indent_str}{key}:")
            lines.append(encode_dict(value, indent + 1))
        elif isinstance(value, list):
            # Array - check if tabular
            if is_tabular(value):
                lines.append(encode_tabular_array(key, value, indent))
            else:
                lines.append(encode_simple_array(key, value, indent))
        else:
            # Simple value
            value_str = encode(value, indent)
            lines.append(f"{indent_str}{key}: {value_str}")
    
    return '\n'.join(lines)


def is_tabular(arr: List[Any]) -> bool:
    """
    Check if array is suitable for tabular format.
    Must be: all objects, same keys, at least 2 items.
    """
    if not arr or len(arr) < 2:
        return False
    
    if not all(isinstance(item, dict) for item in arr):
        return False
    
    # Check all objects have same keys
    first_keys = set(arr[0].keys())
    return all(set(item.keys()) == first_keys for item in arr)


def encode_tabular_array(key: str, arr: List[Dict], indent: int) -> str:
    """
    Encode array as tabular format: [N]{fields}: rows
    """
    indent_str = '  ' * indent
    fields = ','.join(arr[0].keys())
    length = len(arr)
    
    lines = [f"{indent_str}{key}[{length}]{{{fields}}}:"]
    
    for item in arr:
        values = [encode(item[k], 0) for k in arr[0].keys()]
        row = ','.join(values)
        lines.append(f"{indent_str}  {row}")
    
    return '\n'.join(lines)


def encode_simple_array(key: str, arr: List[Any], indent: int) -> str:
    """
    Encode simple array: [N]: val1,val2,val3
    """
    indent_str = '  ' * indent
    length = len(arr)
    
    if all(isinstance(v, (str, int, float, bool, type(None))) for v in arr):
        # Simple values - single line
        values = [encode(v, 0) for v in arr]
        return f"{indent_str}{key}[{length}]: {','.join(values)}"
    else:
        # Complex values - multiple lines
        lines = [f"{indent_str}{key}[{length}]:"]
        for val in arr:
            encoded = encode(val, indent + 1)
            lines.append(encoded if '\n' in encoded else f"{indent_str}  {encoded}")
        return '\n'.join(lines)


def needs_quoting(s: str) -> bool:
    """
    Check if string needs quotes (contains special chars).
    """
    if not s:
        return True
    
    special_chars = [',', ':', '[', ']', '{', '}', '\n', '\t']
    return any(char in s for char in special_chars) or s[0].isspace() or s[-1].isspace()
