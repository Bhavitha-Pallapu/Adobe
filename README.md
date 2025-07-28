Adobe India Hackathon 2025 Solutions

This repository contains the comprehensive solutions developed for the Adobe India Hackathon 2025. The project addresses two main challenges: PDF Outline Extraction (Round 1A) and Persona-Driven Document Intelligence (Round 1B). Both solutions are designed for robustness, scalability, and ease of deployment using Docker.

Project Overview

This hackathon submission tackles critical aspects of document processing and intelligent information retrieval. Round 1A focuses on programmatic extraction of structured outlines from PDF documents, enhancing navigation and accessibility. Round 1B builds upon this by introducing an AI-powered system that provides persona-specific insights and answers from PDF content, leveraging OpenAI's GPT models.

Round 1A: PDF Outline Extraction

Objective

To develop a utility capable of accurately extracting a structured outline (table of contents, headings, subheadings) from any given PDF document. The extracted outline includes the heading text, its hierarchical level (e.g., H1, H2, H3), and the page number where it appears.

Solution Overview

The Round 1A solution is a Python-based command-line utility utilizing PyMuPDF (Fitz) for efficient PDF parsing and text extraction, with pdfplumber as a fallback. It employs a combination of heuristics, including font size analysis, bold text detection, and regular expression matching for common heading patterns, to intelligently identify and categorize headings.

Key Features

• Dual-Engine Extraction: Primary extraction with PyMuPDF for speed and detailed font information, and pdfplumber as a reliable fallback.

• Intelligent Heading Detection: Sophisticated algorithm identifies headings based on font size, font weight (bold), and text patterns (e.g., numbered headings, all-caps titles, academic section names).

• Hierarchical Level Assignment: Assigns appropriate heading levels (H1, H2, H3) based on a combination of font size, text patterns, and document structure.

• Duplicate Removal and Sorting: Ensures a clean and logical outline by removing duplicate entries and sorting headings by page number and then by text length.

• JSON Output: The extracted outline is presented in a structured JSON format for easy integration.

Technical Implementation

• pdf_outline_extractor.py: Contains the core logic, including the PDFOutlineExtractor class with methods for PyMuPDF and pdfplumber based extraction, heading detection, level assignment, and outline cleaning.

• Dockerfile: Defines the Docker environment for consistent execution, built for linux/amd64 architecture. It installs necessary system dependencies (libgl1-mesa-glx) and Python packages.

• requirements.txt: Lists Python dependencies: PyMuPDF, pdfplumber.

Usage

1. Place PDF files: Put your PDF documents into the input directory within the round1a folder.

2. Build Docker Image: Navigate to the round1a directory and build the Docker image:

3. Run Docker Container: Execute the Docker container. The extracted JSON outlines will be saved in the output directory.

Round 1B: Persona-Driven Document Intelligence

Objective

To develop a system that analyzes PDF documents and provides insights tailored to specific user personas. This involves extracting text from PDFs and using an AI model (OpenAI GPT) to generate persona-specific summaries or answer questions based on the document content.

Solution Overview

Round 1B is implemented as a Flask-based RESTful API. It allows users to upload a PDF, specify a persona (student, researcher, business_analyst, general), and optionally provide a specific query. The API extracts text, constructs a prompt for the OpenAI GPT model, and returns the AI's persona-tailored response as a JSON object.

Key Features

• Persona Management: Defines and manages different user personas with unique descriptions, focus areas, and response styles.

• PDF Text Extraction: Reuses robust PDF text extraction logic from Round 1A.

• AI-Powered Analysis: Integrates with OpenAI's GPT models for intelligent document analysis and persona-specific insights.

• Flexible Querying: Supports both general document analysis (summaries, key insights) and specific question-answering.

• RESTful API: Provides a clean API interface with endpoints for document analysis, persona listing, and health checks.

• Docker Support: Containerized for seamless deployment and scalability.

Technical Implementation

• app.py: The Flask application containing the DocumentIntelligence class for persona definitions, PDF text extraction, and AI-driven analysis. It defines API endpoints (/, /health, /personas, /analyze) and handles OpenAI integration and temporary file management.

• Dockerfile: Sets up the Flask application within a linux/amd64 environment, installing system dependencies and Python packages, and exposing port 5000.

• requirements.txt: Lists Python dependencies: Flask, openai, pdfplumber, PyMuPDF, python-dotenv.

Usage

1. Set Environment Variables: Ensure your OpenAI API key and optional API base URL are set as environment variables (OPENAI_API_KEY, OPENAI_API_BASE).

2. Build Docker Image: Navigate to the round1b directory and build the Docker image:

3. Run Docker Container: Run the Docker container, mapping port 5000 and passing your OpenAI environment variables:

4. Access API: The API will be accessible at http://localhost:5000 (or the exposed public URL if using a service like Manus).

Project Structure

Plain Text


Adobe/
├── Hackathon_Solution_Report.md
├── round1a/
│   ├── Dockerfile
│   ├── input/
│   │   ├── Table-Of-Contents-Sample-2021.webp
│   │   ├── file-example_PDF_1MB.webp
│   │   ├── pdf-test.webp
│   │   └── sample.pdf
│   ├── output/
│   │   └── sample.json
│   ├── pdf_outline_extractor.py
│   ├── README.md
│   ├── requirements.txt
│   └── test_round1a.sh
└── round1b/
    ├── Dockerfile
    ├── app.py
    ├── README.md
    └── requirements.txt


Technologies Used

• Python 3.11

• Docker

• PyMuPDF (Fitz)

• pdfplumber

• Flask

• OpenAI GPT (via openai Python library)

• python-dotenv

Testing and Validation

Both solutions were tested with various PDF documents. Round 1A's heading detection and classification were iteratively refined for accuracy. For Round 1B, the API endpoints were verified, and integration points with OpenAI were confirmed, though full end-to-end AI call testing was limited within the sandbox environment.

Conclusion

This project successfully delivers robust and containerized solutions for PDF outline extraction and persona-driven document intelligence, laying a strong foundation for future development and integration.

