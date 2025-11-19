# TOON Format - Python SDK

**Token-Oriented Object Notation** encoder/decoder for Python.

Convert Python dictionaries to TOON format - a compact, human-readable encoding optimized for LLM prompts. Reduces token usage by ~40% compared to JSON while maintaining readability.

## Installation

```bash
pip install toon-format
```

## Quick Start

### Encoding (Python → TOON)

```python
from toon_format import encode

# Simple data
data = {
  "name": "Alice",
  "role": "engineer",
  "active": True
}

print(encode(data))
# Output:
# {
#   name: Alice
#   role: engineer
#   active: true
# }
```

### Decoding (TOON → Python)

```python
from toon_format import decode

toon_str = """
{
  name: Alice
  role: engineer
  active: true
}
"""

data = decode(toon_str)
print(data)
# {'name': 'Alice', 'role': 'engineer', 'active': True}
```

### Round-Trip Conversion

```python
from toon_format import encode, decode

original = {"user": "Alice", "score": 95}
toon_str = encode(original)
restored = decode(toon_str)

assert original == restored  # Perfect round-trip!
```

## Annotation Data Example

Perfect for data annotation workflows:

```python
from toon_format import encode

annotations = [
  {
    "id": 1,
    "text": "Customer wants refund",
    "category": "support",
    "sentiment": "negative",
    "priority": "high"
  },
  {
    "id": 2,
    "text": "Great product quality",
    "category": "feedback",
    "sentiment": "positive",
    "priority": "low"
  }
]

print(encode({"annotations": annotations}))
```

**TOON Output (40% smaller):**

```
{
  annotations: [2]{id,text,category,sentiment,priority}
  [1, "Customer wants refund", support, negative, high]
  [2, "Great product quality", feedback, positive, low]
}
```

## CLI Tool

The SDK includes a command-line tool for easy conversion:

### Convert JSON to TOON

```bash
python -m toon_format.cli convert data.json data.toon
```

### Convert TOON to JSON

```bash
python -m toon_format.cli convert data.toon data.json
```

### Compare Sizes

```bash
python -m toon_format.cli compare data.json

# Output:
# 📊 Size Comparison:
#   JSON: 1,234 chars (~308 tokens)
#   TOON: 789 chars (~197 tokens)
#   Savings: 36.1% (111 tokens)
```

### Print to Stdout

```bash
python -m toon_format.cli convert data.json
# Prints TOON format to stdout
```

## API Reference

### `encode(data, indent=2)`

Convert Python object to TOON format string.

**Parameters:**
- `data`: Python dict, list, or primitive value
- `indent`: Indentation size (default: 2)

**Returns:** TOON format string

**Example:**
```python
result = encode({"key": "value"}, indent=4)
```

### `decode(toon_string)`

Convert TOON format string to Python object.

**Parameters:**
- `toon_string`: TOON format string

**Returns:** Python dict, list, or primitive value

**Raises:** `TOONDecodeError` if invalid TOON format

**Example:**
```python
from toon_format import decode
from toon_format.decoder import TOONDecodeError

try:
  data = decode(toon_str)
except TOONDecodeError as e:
  print(f"Invalid TOON: {e}")
```

## Features

✅ **Full Round-Trip Support** - Encode and decode with perfect fidelity  
✅ **Tabular Arrays** - Compact `[N]{fields}` syntax for structured data  
✅ **40% Token Savings** - Significantly smaller than JSON  
✅ **Human Readable** - Clean, YAML-like syntax  
✅ **Type Preservation** - Maintains strings, numbers, booleans, null  
✅ **Nested Structures** - Full support for nested objects and arrays  
✅ **CLI Tool** - Command-line conversion utilities  
✅ **Comprehensive Tests** - 24 test cases covering all features

## Token Savings Example

For a typical annotation dataset:

- **JSON**: 50,000 tokens/day × 365 days = 18.25M tokens/year
- **TOON**: 30,000 tokens/day × 365 days = 10.95M tokens/year
- **Savings**: 7.3M tokens/year (~$14,600 @ $2/M tokens)

## Testing

Run the test suite:

```bash
cd python-sdk
python -m unittest discover tests
```

Run specific tests:

```bash
python -m unittest tests.test_encoder
python -m unittest tests.test_decoder
```

## Development

```bash
# Clone the repo
git clone https://github.com/swamy18/toon-more.git
cd toon-more/python-sdk

# Install in development mode
pip install -e .

# Run tests
python -m unittest discover tests

# Try the CLI
python -m toon_format.cli --help
```

## License

MIT License - See LICENSE file for details

## Links

- [GitHub Repository](https://github.com/swamy18/toon-more)
- [TOON Specification](https://github.com/toon-format/toon)
- [Python SDK Documentation](https://github.com/swamy18/toon-more/tree/main/python-sdk)
