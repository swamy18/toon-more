#!/usr/bin/env python3
"""Command-line interface for TOON format conversion.

Provides utilities to convert between JSON and TOON formats.
"""

import argparse
import sys
import json
from pathlib import Path
from .encoder import encode
from .decoder import decode, TOONDecodeError


def json_to_toon(input_file, output_file=None, indent=2):
  """Convert JSON file to TOON format.

  Args:
    input_file: Path to input JSON file
    output_file: Path to output TOON file (optional)
    indent: Indentation size (default: 2)
  """
  try:
    with open(input_file, 'r') as f:
      data = json.load(f)

    toon_output = encode(data, indent=indent)

    if output_file:
      with open(output_file, 'w') as f:
        f.write(toon_output)
      print(f"✓ Converted {input_file} to {output_file}")
    else:
      print(toon_output)

  except FileNotFoundError:
    print(f"Error: File '{input_file}' not found", file=sys.stderr)
    sys.exit(1)
  except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in '{input_file}': {e}", file=sys.stderr)
    sys.exit(1)
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)


def toon_to_json(input_file, output_file=None, indent=2, pretty=True):
  """Convert TOON file to JSON format.

  Args:
    input_file: Path to input TOON file
    output_file: Path to output JSON file (optional)
    indent: JSON indentation size (default: 2)
    pretty: Pretty-print JSON (default: True)
  """
  try:
    with open(input_file, 'r') as f:
      toon_content = f.read()

    data = decode(toon_content)

    if pretty:
      json_output = json.dumps(data, indent=indent, ensure_ascii=False)
    else:
      json_output = json.dumps(data, ensure_ascii=False)

    if output_file:
      with open(output_file, 'w') as f:
        f.write(json_output)
      print(f"✓ Converted {input_file} to {output_file}")
    else:
      print(json_output)

  except FileNotFoundError:
    print(f"Error: File '{input_file}' not found", file=sys.stderr)
    sys.exit(1)
  except TOONDecodeError as e:
    print(f"Error: Invalid TOON in '{input_file}': {e}", file=sys.stderr)
    sys.exit(1)
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)


def compare_sizes(json_file):
  """Compare JSON vs TOON file sizes and token counts.

  Args:
    json_file: Path to JSON file to analyze
  """
  try:
    with open(json_file, 'r') as f:
      data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)
    toon_str = encode(data)

    json_size = len(json_str)
    toon_size = len(toon_str)
    savings = ((json_size - toon_size) / json_size) * 100

    # Approximate token count (rough estimate: ~4 chars per token)
    json_tokens = json_size // 4
    toon_tokens = toon_size // 4
    token_savings = json_tokens - toon_tokens

    print("\n📊 Size Comparison:")
    print(f"  JSON: {json_size:,} chars (~{json_tokens:,} tokens)")
    print(f"  TOON: {toon_size:,} chars (~{toon_tokens:,} tokens)")
    print(f"  Savings: {savings:.1f}% ({token_savings:,} tokens)")
    print()

  except FileNotFoundError:
    print(f"Error: File '{json_file}' not found", file=sys.stderr)
    sys.exit(1)
  except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in '{json_file}': {e}", file=sys.stderr)
    sys.exit(1)
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)


def main():
  """Main CLI entry point."""
  parser = argparse.ArgumentParser(
    description='TOON Format Converter - Convert between JSON and TOON formats',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  # Convert JSON to TOON
  toon convert data.json data.toon

  # Convert TOON to JSON
  toon convert data.toon data.json

  # Compare sizes
  toon compare data.json

  # Print to stdout
  toon convert data.json
    """
  )

  subparsers = parser.add_subparsers(dest='command', help='Command to execute')

  # Convert command
  convert_parser = subparsers.add_parser('convert', help='Convert between JSON and TOON formats')
  convert_parser.add_argument('input', type=str, help='Input file path')
  convert_parser.add_argument('output', type=str, nargs='?', help='Output file path (optional)')
  convert_parser.add_argument('--indent', type=int, default=2, help='Indentation size (default: 2)')
  convert_parser.add_argument('--compact', action='store_true', help='Compact JSON output (no indentation)')

  # Compare command
  compare_parser = subparsers.add_parser('compare', help='Compare JSON vs TOON sizes')
  compare_parser.add_argument('json_file', type=str, help='JSON file to analyze')

  args = parser.parse_args()

  if args.command == 'convert':
    input_path = Path(args.input)

    # Detect format from file extension
    if input_path.suffix.lower() == '.json':
      json_to_toon(args.input, args.output, indent=args.indent)
    elif input_path.suffix.lower() in ['.toon', '.txt']:
      toon_to_json(args.input, args.output, indent=args.indent, pretty=not args.compact)
    else:
      print(f"Error: Cannot determine format from extension '{input_path.suffix}'", file=sys.stderr)
      print("Supported extensions: .json, .toon, .txt", file=sys.stderr)
      sys.exit(1)

  elif args.command == 'compare':
    compare_sizes(args.json_file)

  else:
    parser.print_help()
    sys.exit(1)


if __name__ == '__main__':
  main()
