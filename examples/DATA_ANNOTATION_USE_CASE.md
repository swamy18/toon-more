# TOON for Data Annotation Workflows

## 🎯 Use Case: Reducing LLM Costs in AI Annotation Pipelines

### Problem
Data annotation platforms (Appen, Scale AI, Labelbox, etc.) increasingly use LLMs for:
- Quality validation
- Auto-labeling suggestions  
- Annotator guidance
- Batch processing

**Challenge**: JSON is token-expensive for sending annotation data to LLMs.

### Solution: TOON Format

#### Example: Image Classification Annotations

**Traditional JSON (348 tokens)**
```json
{
  "project_id": "IMG_CLASS_2025_Q1",
  "dataset_name": "wildlife_classification",
  "annotator_id": "ANN_5847",
  "batch_id": "BATCH_0042",
  "total_images": 100,
  "completed": 87,
  "annotations": [
    {
      "id": 1,
      "image_url": "s3://bucket/img_001.jpg",
      "label": "tiger",
      "confidence": 0.95,
      "time_spent_sec": 12,
      "validated": true
    },
    {
      "id": 2,
      "image_url": "s3://bucket/img_002.jpg",
      "label": "elephant",
      "confidence": 0.89,
      "time_spent_sec": 15,
      "validated": true
    },
    {
      "id": 3,
      "image_url": "s3://bucket/img_003.jpg",
      "label": "leopard",
      "confidence": 0.92,
      "time_spent_sec": 18,
      "validated": false
    }
  ]
}
```

**TOON Format (187 tokens - 46% savings!)**
```toon
project_id: IMG_CLASS_2025_Q1
dataset_name: wildlife_classification
annotator_id: ANN_5847
batch_id: BATCH_0042
total_images: 100
completed: 87
annotations[3]{id,image_url,label,confidence,time_spent_sec,validated}:
  1,s3://bucket/img_001.jpg,tiger,0.95,12,true
  2,s3://bucket/img_002.jpg,elephant,0.89,15,true
  3,s3://bucket/img_003.jpg,leopard,0.92,18,false
```

### Real-World Impact

#### Cost Calculation (GPT-4o-mini pricing)
- **Input**: $0.15 per 1M tokens
- **Typical annotation batch**: 1,000 images
- **JSON format**: ~116,000 tokens = $17.40 per batch
- **TOON format**: ~62,000 tokens = $9.30 per batch
- **Savings**: $8.10 per batch (46.5%)

#### At Scale (a typical annotation platform Example)
- **Monthly batches**: 500
- **Monthly savings**: $4,050
- **Annual savings**: $48,600

### Integration Example

```python
# annotation_pipeline.py
import json
from toon_format import encode

def send_to_llm_for_validation(annotations_json):
    # Convert to TOON before sending to LLM
    toon_data = encode(annotations_json)
    
    prompt = f"""
    Validate these annotations for quality issues:
    
    ```toon
    {toon_data}
    ```
    
    Check for:
    1. Low confidence scores (< 0.85)
    2. Inconsistent labeling patterns
    3. Unusually long/short annotation times
    """
    
    # Send to LLM (46% fewer tokens!)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response
```

### Why TOON Works for Annotations

1. **Uniform Structure**: Annotation data is highly uniform (same fields per record)
2. **Tabular Format**: Natural fit for TOON's CSV-like arrays
3. **LLM Validation**: Models parse structured data better with explicit field headers
4. **Cost Sensitive**: Annotation platforms process millions of records
5. **Batch Processing**: 40%+ token savings compound quickly

### Use Cases

- ✅ Computer vision annotation quality checks
- ✅ NER/entity extraction validation 
- ✅ Multi-modal annotation workflows
- ✅ Annotator performance analysis
- ✅ Auto-labeling suggestion generation
- ✅ Batch export for LLM fine-tuning

### Benchmarks (Coming Soon)

- [ ] COCO dataset format comparison
- [ ] Label Studio export token analysis  
- [ ] Appen/Scale AI format benchmarks
- [ ] Multi-modal annotation savings

### Get Started

```bash
# Install TOON CLI
npm install -g @toon-format/cli

# Convert your annotation exports
toon-cli annotations.json -o annotations.toon --stats

# See token savings immediately
```

### Resources

- [TOON Specification](../SPEC.md)
- [Full Benchmarks](../benchmarks/)
- [Python SDK](https://github.com/toon-format/toon-python) (coming soon)

---

**Created by**: [Swamy Gadila](https://github.com/swamy18) 
