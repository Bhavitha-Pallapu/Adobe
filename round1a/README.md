# Adobe India Hackathon - Round 1A: PDF Outline Extractor

## Overview

This solution extracts structured outlines from PDF documents, identifying titles and headings (H1, H2, H3) with their corresponding page numbers. The output is formatted as JSON according to the hackathon specifications.

## Approach

### Core Strategy

Our solution uses a multi-library approach to maximize accuracy and reliability:

1. **Primary Method - PyMuPDF (fitz)**: Leverages font formatting information (size, bold flags) to identify headings
2. **Fallback Method - pdfplumber**: Uses text pattern matching when formatting information is insufficient
3. **Hybrid Analysis**: Combines both approaches for optimal results

### Heading Detection Algorithm

The system employs several heuristics to identify headings:

#### Font-Based Detection (PyMuPDF)
- **Font Size Analysis**: Text larger than 12pt is considered potential heading
- **Font Weight**: Bold text combined with size indicates headings
- **Position Analysis**: Text positioning and spacing patterns

#### Pattern-Based Detection (Both Libraries)
- **Numbered Patterns**: `1. Introduction`, `1.1 Methods`, `1.1.1 Details`
- **Keyword Patterns**: `Chapter X`, `Section Y`
- **Case Patterns**: ALL CAPS text, Title Case patterns
- **Length Heuristics**: Short lines (< 80 characters) with specific patterns

#### Level Determination
- **H1**: Chapters, main sections, numbered patterns like `1.`
- **H2**: Subsections, patterns like `1.1`
- **H3**: Sub-subsections, patterns like `1.1.1`

### Libraries and Models Used

- **PyMuPDF (fitz)**: High-performance PDF processing with formatting analysis
- **pdfplumber**: Detailed text extraction and layout analysis
- **pypdf**: Backup for metadata extraction
- **Standard Library**: json, re, pathlib for data processing

No external AI models are used - the solution relies on rule-based heuristics and formatting analysis.

## How to Build and Run

### Building the Docker Image

```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 .
```

### Running the Solution

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:v1.0
```

### Expected Input/Output

**Input**: PDF files in `/app/input/` directory
**Output**: JSON files in `/app/output/` directory with the same base name

**Output Format**:
```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Background",
      "page": 2
    }
  ]
}
```

## Performance Characteristics

- **Processing Speed**: < 10 seconds for 50-page PDFs
- **Memory Usage**: < 200MB per document
- **Accuracy**: Optimized for precision and recall in heading detection
- **Offline Operation**: No internet connectivity required

## Technical Implementation

### Error Handling
- Graceful fallback between libraries
- Robust text cleaning and normalization
- Duplicate removal and sorting

### Optimization Features
- Efficient memory usage with proper resource cleanup
- Fast text processing with compiled regex patterns
- Minimal Docker image size with slim base image

### Multilingual Support
- UTF-8 encoding throughout
- Unicode-aware text processing
- Pattern matching works across languages

## Testing

The solution has been tested with:
- Academic papers with numbered sections
- Technical documents with mixed formatting
- Reports with chapter/section structures
- Documents with various font sizes and styles

## Architecture Decisions

1. **Multi-library approach**: Ensures robustness across different PDF types
2. **Rule-based detection**: More reliable than ML for this specific task
3. **Formatting priority**: Font information is more reliable than text patterns alone
4. **Graceful degradation**: Falls back to simpler methods when advanced features fail

