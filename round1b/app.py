#!/usr/bin/env python3
"""
Adobe India Hackathon - Round 1B: Persona-Driven Document Intelligence
Flask API for persona-driven document analysis and question answering
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify, render_template_string
import openai
import fitz  # PyMuPDF
import pdfplumber
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

class DocumentIntelligence:
    """Persona-driven document intelligence system"""
    
    def __init__(self):
        self.personas = {
            "student": {
                "description": "A student looking for key concepts, definitions, and study materials",
                "focus": "educational content, key terms, summaries, examples",
                "style": "clear, educational, with examples"
            },
            "researcher": {
                "description": "A researcher seeking detailed analysis, methodology, and findings",
                "focus": "research methodology, data analysis, conclusions, citations",
                "style": "analytical, detailed, evidence-based"
            },
            "business_analyst": {
                "description": "A business analyst looking for insights, trends, and actionable information",
                "focus": "business implications, trends, recommendations, metrics",
                "style": "strategic, actionable, business-focused"
            },
            "general": {
                "description": "A general reader seeking overall understanding and key points",
                "focus": "main ideas, key points, general understanding",
                "style": "accessible, comprehensive, well-structured"
            }
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            # Try PyMuPDF first
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            if text.strip():
                return text
            
            # Fallback to pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return text
        
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def analyze_document(self, text: str, persona: str, query: str = None) -> Dict[str, Any]:
        """Analyze document based on persona and optional query"""
        if persona not in self.personas:
            persona = "general"
        
        persona_info = self.personas[persona]
        
        # Prepare the prompt based on persona
        if query:
            prompt = f"""
You are analyzing a document from the perspective of a {persona_info['description']}.

Focus on: {persona_info['focus']}
Response style: {persona_info['style']}

Document text:
{text[:4000]}  # Limit text to avoid token limits

User question: {query}

Please provide a comprehensive answer to the user's question based on the document content, tailored to the {persona} persona. Include relevant quotes and page references where applicable.
"""
        else:
            prompt = f"""
You are analyzing a document from the perspective of a {persona_info['description']}.

Focus on: {persona_info['focus']}
Response style: {persona_info['style']}

Document text:
{text[:4000]}  # Limit text to avoid token limits

Please provide a comprehensive analysis of this document tailored to the {persona} persona. Include:
1. Key insights relevant to this persona
2. Important findings or concepts
3. Actionable information or recommendations
4. Summary of main points

Format your response in a clear, structured manner.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant specializing in document analysis for {persona_info['description']}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "persona": persona,
                "persona_description": persona_info["description"],
                "analysis": analysis,
                "query": query,
                "status": "success"
            }
        
        except Exception as e:
            logger.error(f"Error in document analysis: {str(e)}")
            return {
                "persona": persona,
                "analysis": f"Error analyzing document: {str(e)}",
                "query": query,
                "status": "error"
            }

# Initialize the document intelligence system
doc_intel = DocumentIntelligence()

@app.route('/')
def index():
    """Main page with API documentation"""
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Adobe Hackathon - Round 1B: Persona-Driven Document Intelligence</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .method { color: #007bff; font-weight: bold; }
        .personas { background: #e9f7ef; padding: 15px; border-radius: 5px; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Adobe Hackathon - Round 1B</h1>
        <h2>Persona-Driven Document Intelligence API</h2>
        
        <div class="personas">
            <h3>Available Personas:</h3>
            <ul>
                <li><strong>student</strong>: Focuses on educational content, key terms, and study materials</li>
                <li><strong>researcher</strong>: Seeks detailed analysis, methodology, and findings</li>
                <li><strong>business_analyst</strong>: Looks for insights, trends, and actionable information</li>
                <li><strong>general</strong>: General reader seeking overall understanding</li>
            </ul>
        </div>
        
        <h3>API Endpoints:</h3>
        
        <div class="endpoint">
            <h4><span class="method">POST</span> /analyze</h4>
            <p>Analyze a PDF document with persona-driven intelligence</p>
            <p><strong>Content-Type:</strong> multipart/form-data</p>
            <p><strong>Parameters:</strong></p>
            <ul>
                <li><code>file</code> (required): PDF file to analyze</li>
                <li><code>persona</code> (optional): One of student, researcher, business_analyst, general (default: general)</li>
                <li><code>query</code> (optional): Specific question about the document</li>
            </ul>
        </div>
        
        <div class="endpoint">
            <h4><span class="method">GET</span> /personas</h4>
            <p>Get list of available personas and their descriptions</p>
        </div>
        
        <div class="endpoint">
            <h4><span class="method">GET</span> /health</h4>
            <p>Health check endpoint</p>
        </div>
        
        <h3>Example Usage:</h3>
        <pre>
curl -X POST http://localhost:5000/analyze \\
  -F "file=@document.pdf" \\
  -F "persona=student" \\
  -F "query=What are the main concepts in this document?"
        </pre>
        
        <h3>Example Response:</h3>
        <pre>
{
  "persona": "student",
  "persona_description": "A student looking for key concepts, definitions, and study materials",
  "analysis": "Based on the document analysis...",
  "query": "What are the main concepts in this document?",
  "status": "success"
}
        </pre>
    </div>
</body>
</html>
"""
    return render_template_string(html_template)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "persona-driven-document-intelligence"})

@app.route('/personas', methods=['GET'])
def get_personas():
    """Get available personas"""
    return jsonify({"personas": doc_intel.personas})

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """Analyze uploaded PDF document with persona-driven intelligence"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check file type
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Only PDF files are supported"}), 400
        
        # Get parameters
        persona = request.form.get('persona', 'general')
        query = request.form.get('query', None)
        
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)
        
        try:
            # Extract text from PDF
            text = doc_intel.extract_text_from_pdf(temp_path)
            
            if not text.strip():
                return jsonify({"error": "Could not extract text from PDF"}), 400
            
            # Analyze document
            result = doc_intel.analyze_document(text, persona, query)
            
            return jsonify(result)
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('/tmp', exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

