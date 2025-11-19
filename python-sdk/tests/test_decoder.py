"""Unit tests for TOON decoder."""

import unittest
import sys
import os

# Add parent directory to path to import toon_format
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from toon_format import decode, encode
from toon_format.decoder import TOONDecodeError


class TestTOONDecoder(unittest.TestCase):
  """Test cases for TOON decoding functionality."""

  def test_simple_object(self):
    """Test decoding a simple object."""
    toon_str = """{
  name: John
  age: 30
  active: true
}"""
    result = decode(toon_str)
    self.assertEqual(result['name'], 'John')
    self.assertEqual(result['age'], 30)
    self.assertEqual(result['active'], True)

  def test_nested_object(self):
    """Test decoding nested objects."""
    toon_str = """{
  user: {
    name: Alice
    email: alice@example.com
  }
}"""
    result = decode(toon_str)
    self.assertIn('user', result)
    self.assertEqual(result['user']['name'], 'Alice')
    self.assertEqual(result['user']['email'], 'alice@example.com')

  def test_primitives(self):
    """Test decoding primitive values."""
    toon_str = """{
  string: hello
  number: 42
  float: 3.14
  boolean: false
  null: null
}"""
    result = decode(toon_str)
    self.assertEqual(result['string'], 'hello')
    self.assertEqual(result['number'], 42)
    self.assertEqual(result['float'], 3.14)
    self.assertEqual(result['boolean'], False)
    self.assertIsNone(result['null'])

  def test_quoted_strings(self):
    """Test decoding quoted strings."""
    toon_str = """{
  needs_quotes: "hello world"
  with_comma: "red,blue"
  with_colon: "key:value"
}"""
    result = decode(toon_str)
    self.assertEqual(result['needs_quotes'], 'hello world')
    self.assertEqual(result['with_comma'], 'red,blue')
    self.assertEqual(result['with_colon'], 'key:value')

  def test_simple_array(self):
    """Test decoding simple inline arrays."""
    toon_str = """{
  tags: [python, toon, encoding]
}"""
    result = decode(toon_str)
    self.assertEqual(result['tags'], ['python', 'toon', 'encoding'])

  def test_tabular_array(self):
    """Test decoding tabular arrays."""
    toon_str = """{
  users: [3]{id,name,score}
  [1, Alice, 95]
  [2, Bob, 87]
  [3, Charlie, 92]
}"""
    result = decode(toon_str)
    self.assertIn('users', result)
    self.assertEqual(len(result['users']), 3)
    self.assertEqual(result['users'][0]['id'], 1)
    self.assertEqual(result['users'][0]['name'], 'Alice')
    self.assertEqual(result['users'][0]['score'], 95)
    self.assertEqual(result['users'][1]['name'], 'Bob')

  def test_mixed_array(self):
    """Test decoding arrays with mixed types."""
    toon_str = """{
  mixed: [1, text, true, null, 3.14]
}"""
    result = decode(toon_str)
    self.assertEqual(result['mixed'], [1, 'text', True, None, 3.14])

  def test_empty_structures(self):
    """Test decoding empty objects and arrays."""
    toon_str = """{
  empty_obj: {}
  empty_array: []
}"""
    result = decode(toon_str)
    self.assertEqual(result['empty_obj'], {})
    self.assertEqual(result['empty_array'], [])

  def test_round_trip(self):
    """Test that encode -> decode produces the same data."""
    original = {
      "name": "John Doe",
      "age": 30,
      "email": "john@example.com",
      "active": True,
      "score": 95.5,
      "tags": ["python", "developer"],
      "metadata": {
        "created": "2024-01-01",
        "updated": "2024-01-15"
      }
    }
    toon_str = encode(original)
    result = decode(toon_str)
    self.assertEqual(result, original)

  def test_round_trip_tabular(self):
    """Test round trip with tabular arrays."""
    original = {
      "users": [
        {"id": 1, "name": "Alice", "score": 95},
        {"id": 2, "name": "Bob", "score": 87},
        {"id": 3, "name": "Charlie", "score": 92}
      ]
    }
    toon_str = encode(original)
    result = decode(toon_str)
    self.assertEqual(result, original)

  def test_invalid_format(self):
    """Test that invalid TOON raises an error."""
    with self.assertRaises(TOONDecodeError):
      decode("not valid toon")

  def test_missing_closing_brace(self):
    """Test that missing closing brace raises an error."""
    toon_str = """{
  name: John
  age: 30
"""
    with self.assertRaises(TOONDecodeError):
      decode(toon_str)

  def test_deeply_nested(self):
    """Test decoding deeply nested structures."""
    toon_str = """{
  level1: {
    level2: {
      level3: {
        value: deep
      }
    }
  }
}"""
    result = decode(toon_str)
    self.assertEqual(result['level1']['level2']['level3']['value'], 'deep')


if __name__ == '__main__':
  unittest.main()
