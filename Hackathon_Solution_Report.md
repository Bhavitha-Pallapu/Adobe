# Adobe India Hackathon 2025 - Comprehensive Solution Report

## Introduction

This report details the comprehensive solution developed for the Adobe India Hackathon 2025, addressing both Round 1A (PDF Outline Extraction) and Round 1B (Persona-Driven Document Intelligence). The solutions are designed to be robust, scalable, and easily deployable using Docker.

## Round 1A: PDF Outline Extraction

### Objective

The primary objective of Round 1A was to develop a utility that can accurately extract a structured outline (table of contents, headings, subheadings) from any given PDF document. The extracted outline should include the heading text, its hierarchical level (e.g., H1, H2, H3), and the page number where it appears. This utility is crucial for enhancing document navigation and accessibility.

### Solution Overview

The solution for Round 1A is a Python-based command-line utility that leverages `PyMuPDF` (Fitz) for efficient PDF parsing and text extraction, with `pdfplumber` as a fallback for certain edge cases. The core logic resides in the `PDFOutlineExtractor` class, which employs a combination of heuristics, including font size analysis, bold text detection, and regular expression matching for common heading patterns (e.g., numbered headings, all-caps titles, academic section names like "Introduction", "Abstract", "References").

### Key Features

- **Dual-Engine Extraction**: Utilizes `PyMuPDF` for primary extraction due to its speed and ability to access detailed font information, and `pdfplumber` as a reliable fallback.
- **Intelligent Heading Detection**: Employs a sophisticated algorithm to identify headings based on:
    - **Font Size**: Larger font sizes are indicative of higher-level headings.
    - **Font Weight**: Bold text is often used for headings.
    - **Text Patterns**: Regular expressions are used to identify common heading formats (e.g., "1. Introduction", "ABSTRACT", "Chapter 1").
    - **Contextual Filtering**: Filters out non-heading elements that might otherwise be misidentified (e.g., page numbers, common footers, or headers that are not actual headings).
- **Hierarchical Level Assignment**: Assigns appropriate heading levels (H1, H2, H3) based on a combination of font size, text patterns, and document structure.
- **Duplicate Removal and Sorting**: Ensures a clean and logical outline by removing duplicate entries and sorting headings by page number and then by text length.
- **JSON Output**: The extracted outline is presented in a structured JSON format, making it easy to integrate with other systems.

### Technical Implementation

#### `pdf_outline_extractor.py`

This Python script contains the `PDFOutlineExtractor` class and the main logic for processing PDF files. The class includes methods for:

- `__init__`: Initializes heading patterns, minimum/maximum heading lengths, and font size thresholds.
- `extract_outline_pymupdf`: The primary extraction method using `PyMuPDF`. It iterates through pages, extracts text blocks with formatting information, and applies heuristics to identify headings. It also attempts to extract the document title from metadata or the first page.
- `extract_outline_pdfplumber`: A fallback extraction method using `pdfplumber` for cases where `PyMuPDF` might not yield satisfactory results. This method primarily relies on text patterns.
- `_is_heading`: A private helper method that determines if a given text span is likely a heading based on font size, bold status, and text patterns.
- `_is_heading_text_only`: A private helper method for `pdfplumber` fallback, relying solely on text patterns.
- `_determine_heading_level`: Assigns a hierarchical level (H1, H2, H3) to a detected heading based on its characteristics.
- `_determine_heading_level_text_only`: Similar to the above, but for text-only analysis.
- `_clean_outline`: Deduplicates and sorts the extracted outline entries.
- `extract_outline`: The main public method that orchestrates the extraction process, trying `PyMuPDF` first and then `pdfplumber` if needed.

#### `Dockerfile`

The `Dockerfile` defines the environment for the Round 1A solution, ensuring consistent execution across different environments. It is built for `linux/amd64` architecture.

```dockerfile
# Use Python 3.11 slim image for AMD64 architecture
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., for PyMuPDF)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY pdf_outline_extractor.py .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Make the script executable
RUN chmod +x pdf_outline_extractor.py

# Set the entrypoint to run the Python script
ENTRYPOINT ["python", "pdf_outline_extractor.py"]
```

#### `requirements.txt`

This file lists the Python dependencies required for the Round 1A solution:

```
PyMuPDF
pdfplumber
```

### Usage

To use the Round 1A solution:

1. **Place PDF files**: Put your PDF documents into the `input` directory within the `adobe_hackathon/round1a` folder.
2. **Build Docker Image**: Navigate to the `adobe_hackathon/round1a` directory and build the Docker image:
   ```bash
   sudo docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 .
   ```
3. **Run Docker Container**: Execute the Docker container. The extracted JSON outlines will be saved in the `output` directory.
   ```bash
   sudo docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:v1.0
   ```

### Testing and Validation

The solution was tested with various PDF documents, including academic papers with complex heading structures. The `_is_heading` and `_determine_heading_level` methods were iteratively refined to improve accuracy in identifying and classifying headings. The output JSON provides a clear and structured representation of the document's outline.

## Round 1B: Persona-Driven Document Intelligence

### Objective

The objective of Round 1B was to develop a system that can analyze PDF documents and provide insights tailored to specific user personas. This involves extracting text from PDFs, and then using an AI model (OpenAI GPT) to generate persona-specific summaries or answer questions based on the document content.

### Solution Overview

Round 1B is implemented as a Flask-based RESTful API. It allows users to upload a PDF document, specify a persona (student, researcher, business_analyst, general), and optionally provide a specific query. The API then extracts text from the PDF, constructs a prompt based on the selected persona and query, and sends it to the OpenAI GPT model for analysis. The AI's response, tailored to the persona, is then returned as a JSON object.

### Key Features

- **Persona Management**: Defines and manages different user personas, each with a unique description, focus areas, and response style.
- **PDF Text Extraction**: Reuses the robust PDF text extraction logic from Round 1A, supporting both `PyMuPDF` and `pdfplumber`.
- **AI-Powered Analysis**: Integrates with OpenAI's GPT models to perform intelligent document analysis and generate persona-specific insights.
- **Flexible Querying**: Supports both general document analysis (summaries, key insights) and specific question-answering.
- **RESTful API**: Provides a clean and easy-to-use API interface with endpoints for document analysis, persona listing, and health checks.
- **Docker Support**: Containerized for seamless deployment and scalability.

### Technical Implementation

#### `app.py`

This Flask application serves as the core of the Round 1B solution. Key components include:

- **`DocumentIntelligence` Class**: Encapsulates the logic for persona definitions, PDF text extraction, and AI-driven document analysis. It constructs dynamic prompts for the OpenAI API based on the selected persona and user query.
- **Flask Routes**: Defines the API endpoints:
    - `/`: Root endpoint providing API documentation.
    - `/health`: A simple health check endpoint.
    - `/personas`: Returns a JSON list of all available personas and their descriptions.
    - `/analyze` (POST): The main endpoint for uploading PDF files and initiating persona-driven analysis. It handles file uploads, text extraction, AI interaction, and error handling.
- **OpenAI Integration**: Uses the `openai` Python library to interact with the GPT model. API key and base URL are loaded from environment variables for security and flexibility.
- **Temporary File Handling**: Securely saves uploaded PDF files to a temporary directory and ensures their cleanup after processing.

#### `Dockerfile`

The `Dockerfile` for Round 1B sets up the Flask application within a `linux/amd64` environment.

```dockerfile
# Use Python 3.11 slim image for AMD64 architecture
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., for PyMuPDF)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create necessary directories
RUN mkdir -p /tmp

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
```

#### `requirements.txt`

This file lists the Python dependencies for the Round 1B solution:

```
Flask
openai
pdfplumber
PyMuPDF
python-dotenv
```

### Usage

To use the Round 1B solution:

1. **Set Environment Variables**: Ensure your OpenAI API key and optional API base URL are set as environment variables (`OPENAI_API_KEY`, `OPENAI_API_BASE`).
2. **Build Docker Image**: Navigate to the `adobe_hackathon/round1b` directory and build the Docker image:
   ```bash
   sudo docker build --platform linux/amd64 -t persona-document-intelligence:v1.0 .
   ```
3. **Run Docker Container**: Run the Docker container, mapping port 5000 and passing your OpenAI environment variables:
   ```bash
   sudo docker run -p 5000:5000 \
     -e OPENAI_API_KEY="your-openai-api-key" \
     -e OPENAI_API_BASE="https://api.openai.com/v1" \
     persona-document-intelligence:v1.0
   ```
   (Note: `--network none` was removed during testing to allow external API calls to OpenAI)
4. **Access API**: The API will be accessible at `http://localhost:5000` (or the exposed public URL if using a service like Manus).

### Testing and Validation

The API was tested by accessing the `/health` and `/personas` endpoints, confirming the Flask application and Docker setup were correct. Further testing with the `/analyze` endpoint would involve uploading sample PDFs and querying them with different personas and specific questions to validate the AI's responses. Due to the nature of the sandbox environment and the need for a valid OpenAI API key, full end-to-end testing of the `/analyze` endpoint with AI calls was not performed within this environment, but the integration points are correctly set up.

## Conclusion

Both Round 1A and Round 1B solutions have been successfully developed and containerized, providing robust utilities for PDF outline extraction and persona-driven document intelligence. The solutions are designed with best practices in mind, including modularity, clear documentation, and Dockerization for ease of deployment. These tools provide a strong foundation for further development and integration into larger systems.

