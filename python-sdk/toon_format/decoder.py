"""TOON Format Decoder - Parses TOON format into Python dictionaries.

This module provides functionality to decode TOON (Token-Oriented Object Notation)
format strings back into Python data structures.
"""

import re
from typing import Any, List, Dict, Tuple


class TOONDecodeError(Exception):
  """Exception raised when TOON decoding fails."""
  pass


class TOONDecoder:
  """Decoder for TOON format strings."""

  def __init__(self, toon_string: str):
    self.lines = toon_string.strip().split('\n')
    self.current_line = 0
    self.indent_size = 2  # Default to 2-space indentation

  def decode(self) -> Any:
    """Decode TOON string into Python object."""
    if not self.lines:
      raise TOONDecodeError("Empty TOON string")

    # Detect if it's an array or object at root level
    first_line = self.lines[0].strip()
    if first_line.startswith('['):
      return self._decode_array(0, 0)
    elif first_line == '{':
      return self._decode_object(0, 0)
    else:
      raise TOONDecodeError(f"Invalid TOON format: expected '{{' or '[', got '{first_line}'")

  def _get_indent_level(self, line: str) -> int:
    """Get the indentation level of a line."""
    return len(line) - len(line.lstrip())

  def _decode_object(self, start_line: int, expected_indent: int) -> Dict[str, Any]:
    """Decode an object from TOON format."""
    result = {}
    self.current_line = start_line + 1  # Skip opening '{'

    while self.current_line < len(self.lines):
      line = self.lines[self.current_line]
      indent = self._get_indent_level(line)
      content = line.strip()

      # Check for closing brace
      if content == '}':
        return result

      # Parse key-value pair
      if ':' not in content:
        raise TOONDecodeError(f"Line {self.current_line + 1}: Expected key-value pair, got '{content}'")

      key, value_part = content.split(':', 1)
      key = key.strip()
      value_part = value_part.strip()

      # Remove quotes from key if present
      if key.startswith('"') and key.endswith('"'):
        key = key[1:-1]

      # Parse the value
      if value_part == '{':
        # Nested object
        result[key] = self._decode_object(self.current_line, indent + self.indent_size)
      elif value_part.startswith('['):
        # Array
        result[key], self.current_line = self._decode_array_inline(self.current_line, value_part)
      else:
        # Primitive value
        result[key] = self._parse_primitive(value_part)

      self.current_line += 1

    raise TOONDecodeError("Unexpected end of object")

  def _decode_array_inline(self, start_line: int, first_value: str) -> Tuple[List[Any], int]:
    """Decode an array that might be inline or multi-line."""
    # Check if it's a tabular array header like [3]{field1,field2}
    tabular_match = re.match(r'\[(\d+)\]\{([^}]+)\}', first_value)
    if tabular_match:
      return self._decode_tabular_array(start_line, tabular_match)

    # Check if it's a simple inline array like [1, 2, 3]
    if first_value.startswith('[') and first_value.endswith(']'):
      # Parse inline array
      content = first_value[1:-1].strip()
      if not content:
        return [], start_line
      
      items = self._split_array_items(content)
      return [self._parse_primitive(item.strip()) for item in items], start_line

    # Multi-line array
    return self._decode_array_multiline(start_line)

  def _decode_tabular_array(self, start_line: int, match: re.Match) -> Tuple[List[Dict], int]:
    """Decode a tabular array format like [3]{field1,field2}."""
    count = int(match.group(1))
    fields = [f.strip() for f in match.group(2).split(',')]
    
    result = []
    line_idx = start_line + 1
    
    for _ in range(count):
      if line_idx >= len(self.lines):
        raise TOONDecodeError(f"Tabular array: expected {count} rows, got fewer")
      
      line = self.lines[line_idx].strip()
      if not line.startswith('[') or not line.endswith(']'):
        raise TOONDecodeError(f"Line {line_idx + 1}: Expected array row, got '{line}'")
      
      values_str = line[1:-1].strip()
      values = self._split_array_items(values_str)
      
      if len(values) != len(fields):
        raise TOONDecodeError(
          f"Line {line_idx + 1}: Expected {len(fields)} values, got {len(values)}"
        )
      
      row = {}
      for field, value in zip(fields, values):
        row[field] = self._parse_primitive(value.strip())
      
      result.append(row)
      line_idx += 1
    
    return result, line_idx - 1

  def _decode_array_multiline(self, start_line: int) -> Tuple[List[Any], int]:
    """Decode a multi-line array."""
    result = []
    line_idx = start_line + 1
    start_indent = self._get_indent_level(self.lines[start_line])

    while line_idx < len(self.lines):
      line = self.lines[line_idx]
      indent = self._get_indent_level(line)
      content = line.strip()

      if content == ']':
        return result, line_idx

      # Check if this is a nested structure
      if content == '{':
        result.append(self._decode_object(line_idx, indent + self.indent_size))
      elif content.startswith('['):
        nested_array, line_idx = self._decode_array_inline(line_idx, content)
        result.append(nested_array)
      else:
        # Remove trailing comma if present
        if content.endswith(','):
          content = content[:-1].strip()
        result.append(self._parse_primitive(content))

      line_idx += 1

    raise TOONDecodeError("Unexpected end of array")

  def _split_array_items(self, content: str) -> List[str]:
    """Split array items respecting nested structures and quoted strings."""
    items = []
    current = []
    depth = 0
    in_quotes = False
    escape_next = False

    for char in content:
      if escape_next:
        current.append(char)
        escape_next = False
        continue

      if char == '\\':
        escape_next = True
        current.append(char)
        continue

      if char == '"':
        in_quotes = not in_quotes
        current.append(char)
        continue

      if not in_quotes:
        if char in '[{':
          depth += 1
        elif char in ']}':
          depth -= 1
        elif char == ',' and depth == 0:
          items.append(''.join(current))
          current = []
          continue

      current.append(char)

    if current:
      items.append(''.join(current))

    return items

  def _parse_primitive(self, value: str) -> Any:
    """Parse a primitive value from TOON format."""
    value = value.strip()

    # Handle null
    if value == 'null':
      return None

    # Handle booleans
    if value == 'true':
      return True
    if value == 'false':
      return False

    # Handle quoted strings
    if value.startswith('"') and value.endswith('"'):
      # Unescape the string
      return value[1:-1].replace('\\"', '"').replace('\\\\', '\\')

    # Handle numbers
    try:
      if '.' in value:
        return float(value)
      return int(value)
    except ValueError:
      # If all else fails, treat as unquoted string
      return value


def decode(toon_string: str) -> Any:
  """Decode a TOON format string into a Python object.

  Args:
    toon_string: TOON format string to decode

  Returns:
    Python object (dict, list, or primitive)

  Raises:
    TOONDecodeError: If the TOON string is invalid

  Example:
    >>> toon_str = '''
    ... {
    ...   name: "John"
    ...   age: 30
    ... }
    ... '''
    >>> result = decode(toon_str)
    >>> print(result)
    {'name': 'John', 'age': 30}
  """
  decoder = TOONDecoder(toon_string)
  return decoder.decode()
