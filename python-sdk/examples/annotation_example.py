#!/usr/bin/env python3
"""Example: Using TOON for Data Annotation Workflows

Demonstrates token savings when sending annotation data to LLMs.
"""

import sys
import json
sys.path.insert(0, '..')

from toon_format import encode


def main():
    # Sample annotation data (typical from Label Studio, Labelbox, etc.)
    annotation_batch = {
        "project_id": "wildlife_classification_2025",
        "annotator_id": "ANN_5847",
        "batch_id": "BATCH_0042",
        "created_at": "2025-11-19T10:00:00Z",
        "annotations": [
            {
                "id": 1,
                "image_url": "s3://bucket/images/img_001.jpg",
                "label": "tiger",
                "confidence": 0.95,
                "time_spent_sec": 12,
                "validated": True,
                "annotator_notes": "Clear visibility"
            },
            {
                "id": 2,
                "image_url": "s3://bucket/images/img_002.jpg",
                "label": "elephant",
                "confidence": 0.89,
                "time_spent_sec": 15,
                "validated": True,
                "annotator_notes": "Partial occlusion"
            },
            {
                "id": 3,
                "image_url": "s3://bucket/images/img_003.jpg",
                "label": "leopard",
                "confidence": 0.92,
                "time_spent_sec": 18,
                "validated": False,
                "annotator_notes": "Needs review"
            },
        ]
    }

    print("=" * 70)
    print("TOON Format - Annotation Data Example")
    print("=" * 70)
    print()

    # Convert to JSON (traditional approach)
    json_str = json.dumps(annotation_batch, indent=2)
    json_tokens = len(json_str.split())  # Rough estimate

    # Convert to TOON
    toon_str = encode(annotation_batch)
    toon_tokens = len(toon_str.split())  # Rough estimate

    # Display both formats
    print("📄 JSON Format (Traditional):")
    print("-" * 70)
    print(json_str)
    print()
    print(f"Approximate tokens: {json_tokens}")
    print()

    print("🎒 TOON Format (Optimized):")
    print("-" * 70)
    print(toon_str)
    print()
    print(f"Approximate tokens: {toon_tokens}")
    print()

    # Calculate savings
    savings_pct = ((json_tokens - toon_tokens) / json_tokens) * 100
    print("=" * 70)
    print(f"💰 Token Savings: ~{savings_pct:.1f}%")
    print(f"📊 Tokens saved: {json_tokens - toon_tokens}")
    print()
    print("At GPT-4o-mini rates ($0.15 per 1M input tokens):")
    
    # Scale to realistic batch size
    batch_size = 1000
    json_cost = (json_tokens * batch_size / 1_000_000) * 0.15
    toon_cost = (toon_tokens * batch_size / 1_000_000) * 0.15
    savings_per_batch = json_cost - toon_cost
    
    print(f"  JSON cost (1,000 records): ${json_cost:.2f}")
    print(f"  TOON cost (1,000 records): ${toon_cost:.2f}")
    print(f"  Savings per batch: ${savings_per_batch:.2f}")
    print()
    print(f"📈 Annual savings (500 batches/month): ${savings_per_batch * 500 * 12:,.2f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
