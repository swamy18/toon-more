# TOON Format - Python SDK

**Token-Oriented Object Notation** encoder for Python.

Convert Python dictionaries to TOON format - a compact, human-readable encoding optimized for LLM prompts. Reduces token usage by ~40% compared to JSON while maintaining readability.

## Installation

```bash
pip install toon-format
```

## Quick Start

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
# name: Alice
# role: engineer
# active: true
```

## Annotation Data Example

Perfect for data annotation workflows:

```python
from toon_format import encode

annotations = {
    "project": "wildlife_classification",
    "annotator": "ANN_001",
    "data": [
        {"id": 1, "image": "img_001.jpg", "label": "tiger", "confidence": 0.95},
        {"id": 2, "image": "img_002.jpg", "label": "elephant", "confidence": 0.89},
        {"id": 3, "image": "img_003.jpg", "label": "leopard", "confidence": 0.92}
    ]
}

print(encode(annotations))
```

**Output (TOON format):**
```toon
project: wildlife_classification
annotator: ANN_001
data[3]{id,image,label,confidence}:
  1,img_001.jpg,tiger,0.95
  2,img_002.jpg,elephant,0.89
  3,img_003.jpg,leopard,0.92
```

## Features

- **Tabular Arrays**: Automatically detects uniform arrays and formats as tables
- **Type Handling**: Supports strings, numbers, booleans, null, nested objects
- **Indentation**: Clean 2-space indentation for nested structures
- **Smart Quoting**: Only quotes strings when necessary (special characters)
- **Field Headers**: `[N]{fields}` syntax for array metadata

## Use Cases

✅ **Data Annotation Pipelines** - Reduce LLM costs for quality validation  
✅ **AI Training Data** - Compact representation for fine-tuning datasets  
✅ **Prompt Engineering** - Fit more context in token limits  
✅ **API Responses** - Token-efficient format for LLM consumption  

## Token Savings

**Example: 100 annotation records**
- JSON: ~116,000 tokens ($17.40 @ GPT-4o-mini)
- TOON: ~62,000 tokens ($9.30)
- **Savings: 46% fewer tokens, $8.10 per batch**

## API Reference

### `encode(data, indent=0)`

Convert Python data to TOON format.

**Parameters:**
- `data`: Dict, list, or primitive value to encode
- `indent`: Starting indentation level (default: 0)

**Returns:**
- String in TOON format

**Example:**
```python
from toon_format import encode

result = encode({"users": [{"name": "Alice"}, {"name": "Bob"}]})
print(result)
# users[2]{name}:
#   Alice
#   Bob
```

## Spec Compliance

Follows [TOON Specification v2.0](https://github.com/toon-format/spec/blob/main/SPEC.md)

## Contributing

Contributions welcome! This is an open-source implementation.

## License

MIT License

## Links

- [TOON Specification](https://github.com/toon-format/spec)
- [Main TOON Repository](https://github.com/toon-format/toon)
- [Benchmarks](https://github.com/toon-format/toon/tree/main/benchmarks)
- [TypeScript SDK](https://www.npmjs.com/package/@toon-format/toon)

---

**Created by**: [@swamy18](https://github.com/swamy18)  
**Status**: Alpha - Encoder complete, decoder in progress
