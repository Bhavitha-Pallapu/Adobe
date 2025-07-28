# Adobe India Hackathon - Round 1B: Persona-Driven Document Intelligence

This solution provides a Flask-based API for persona-driven document analysis and question answering using PDF documents.

## Features

- **Persona-Driven Analysis**: Tailored document analysis based on different user personas
- **PDF Text Extraction**: Robust PDF text extraction using PyMuPDF and pdfplumber
- **AI-Powered Insights**: Uses OpenAI GPT models for intelligent document analysis
- **RESTful API**: Clean REST API for easy integration
- **Docker Support**: Containerized for easy deployment

## Available Personas

1. **Student**: Focuses on educational content, key terms, and study materials
2. **Researcher**: Seeks detailed analysis, methodology, and findings
3. **Business Analyst**: Looks for insights, trends, and actionable information
4. **General**: General reader seeking overall understanding

## API Endpoints

### POST /analyze
Analyze a PDF document with persona-driven intelligence.

**Parameters:**
- `file` (required): PDF file to analyze
- `persona` (optional): One of student, researcher, business_analyst, general (default: general)
- `query` (optional): Specific question about the document

**Example:**
```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@document.pdf" \
  -F "persona=student" \
  -F "query=What are the main concepts in this document?"
```

### GET /personas
Get list of available personas and their descriptions.

### GET /health
Health check endpoint.

## Setup and Running

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"  # Optional
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build --platform linux/amd64 -t persona-document-intelligence:v1.0 .
```

2. Run the container:
```bash
docker run -p 5000:5000 \
  -e OPENAI_API_KEY="your-openai-api-key" \
  --network none \
  persona-document-intelligence:v1.0
```

## Requirements

- Python 3.11+
- OpenAI API key
- PDF documents for analysis

## Dependencies

- Flask: Web framework
- openai: OpenAI API client
- pdfplumber: PDF text extraction
- PyMuPDF: Alternative PDF processing
- python-dotenv: Environment variable management

## Architecture

The solution consists of:

1. **DocumentIntelligence Class**: Core logic for PDF processing and AI analysis
2. **Flask API**: RESTful endpoints for document analysis
3. **Persona System**: Different analysis perspectives based on user roles
4. **PDF Processing**: Robust text extraction from PDF documents
5. **AI Integration**: OpenAI GPT models for intelligent analysis

## Error Handling

The API includes comprehensive error handling for:
- Invalid file formats
- PDF processing errors
- AI API failures
- Missing parameters

## Security Considerations

- File uploads are temporarily stored and cleaned up
- Input validation for file types and parameters
- Environment variable management for API keys
- No persistent storage of uploaded documents

