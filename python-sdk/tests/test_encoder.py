"""Unit tests for TOON encoder."""

import unittest
import sys
import os

# Add parent directory to path to import toon_format
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from toon_format import encode


class TestTOONEncoder(unittest.TestCase):
  """Test cases for TOON encoding functionality."""

  def test_simple_object(self):
    """Test encoding a simple object."""
    data = {
      "name": "John",
      "age": 30,
      "active": True
    }
    result = encode(data)
    self.assertIn("name: John", result)
    self.assertIn("age: 30", result)
    self.assertIn("active: true", result)

  def test_nested_object(self):
    """Test encoding nested objects."""
    data = {
      "user": {
        "name": "Alice",
        "email": "alice@example.com"
      }
    }
    result = encode(data)
    self.assertIn("user: {", result)
    self.assertIn("name: Alice", result)
    self.assertIn("email: alice@example.com", result)

  def test_array_encoding(self):
    """Test encoding arrays."""
    data = {
      "tags": ["python", "toon", "encoding"]
    }
    result = encode(data)
    self.assertIn("tags: [", result)
    self.assertIn("python", result)
    self.assertIn("toon", result)

  def test_tabular_array(self):
    """Test encoding tabular arrays."""
    data = {
      "users": [
        {"id": 1, "name": "Alice", "score": 95},
        {"id": 2, "name": "Bob", "score": 87},
        {"id": 3, "name": "Charlie", "score": 92}
      ]
    }
    result = encode(data)
    # Should use tabular format [3]{id,name,score}
    self.assertIn("[3]{", result)
    self.assertIn("id", result)
    self.assertIn("name", result)
    self.assertIn("score", result)

  def test_primitives(self):
    """Test encoding primitive values."""
    data = {
      "string": "hello",
      "number": 42,
      "float": 3.14,
      "boolean": False,
      "null": None
    }
    result = encode(data)
    self.assertIn("string: hello", result)
    self.assertIn("number: 42", result)
    self.assertIn("float: 3.14", result)
    self.assertIn("boolean: false", result)
    self.assertIn("null: null", result)

  def test_string_quoting(self):
    """Test proper quoting of strings."""
    data = {
      "needs_quotes": "hello world",
      "with_comma": "red,blue",
      "with_colon": "key:value",
      "simple": "hello"
    }
    result = encode(data)
    self.assertIn('needs_quotes: "hello world"', result)
    self.assertIn('with_comma: "red,blue"', result)
    self.assertIn('with_colon: "key:value"', result)

  def test_empty_structures(self):
    """Test encoding empty objects and arrays."""
    data = {
      "empty_obj": {},
      "empty_array": []
    }
    result = encode(data)
    self.assertIn("empty_obj: {}", result)
    self.assertIn("empty_array: []", result)

  def test_mixed_array(self):
    """Test encoding arrays with mixed types."""
    data = {
      "mixed": [1, "text", True, None, 3.14]
    }
    result = encode(data)
    self.assertIn("mixed: [", result)
    self.assertIn("1", result)
    self.assertIn("text", result)
    self.assertIn("true", result)
    self.assertIn("null", result)
    self.assertIn("3.14", result)

  def test_indentation(self):
    """Test proper indentation."""
    data = {
      "outer": {
        "inner": {
          "value": 42
        }
      }
    }
    result = encode(data, indent=2)
    lines = result.split('\n')
    # Check that nested structures have proper indentation
    self.assertTrue(any(line.startswith('  ') for line in lines))
    self.assertTrue(any(line.startswith('    ') for line in lines))

  def test_compact_output(self):
    """Test compact output without extra spacing."""
    data = {"key": "value"}
    result = encode(data)
    # Should not have unnecessary blank lines
    self.assertNotIn('\n\n\n', result)


if __name__ == '__main__':
  unittest.main()
