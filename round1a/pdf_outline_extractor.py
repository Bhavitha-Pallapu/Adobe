#!/usr/bin/env python3
"""
Adobe India Hackathon - Round 1A: PDF Outline Extractor
Extracts structured outline (Title, H1, H2, H3 headings) from PDF files
"""

import os
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import fitz  # PyMuPDF
import pdfplumber


class PDFOutlineExtractor:
    """Extract structured outline from PDF documents"""
    
    def __init__(self):
        self.heading_patterns = [
            # Academic paper specific patterns
            r"^(\d+\.\d+\.\d+\s+.*)$",  # 1.1.1 Sub-subsection
            r"^(\d+\.\d+\s+.*)$",      # 1.1 Subsection
            r"^(\d+\.\s+.*)$",          # 1. Introduction
            r"^(Abstract|Introduction|Literature Review|Method|Methods|Results|Findings|Discussion|Conclusion|Conclusions|References|Bibliography|Acknowledgements)$", # Common section titles
            # General heading patterns
            r"^([A-Z][A-Z\s]+)$",      # ALL CAPS HEADINGS
            r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)$",  # Title Case Headings
            r"^(Chapter\s+\d+[:\s]*.*)$",  # Chapter headings
            r"^(Section\s+\d+[:\s]*.*)$",  # Section headings
        ]
        self.min_heading_length = 3
        self.max_heading_length = 100
        self.font_size_thresholds = {
            "H1": 20,  # Example threshold for H1
            "H2": 16,  # Example threshold for H2
            "H3": 12   # Example threshold for H3
        }
        self.min_font_size_for_heading = 10 # Minimum font size to be considered a heading
    
    def extract_outline_pymupdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract outline using PyMuPDF (primary method)"""
        doc = fitz.open(pdf_path)
        outline = []
        title = ""
        
        try:
            # Try to get title from metadata
            metadata = doc.metadata
            if metadata and metadata.get("title"):
                title = metadata["title"].strip()
            
            # If no title in metadata, try to extract from first page
            if not title:
                first_page = doc[0]
                text = first_page.get_text()
                lines = text.split("\n")
                for line in lines[:10]:  # Check first 10 lines
                    line = line.strip()
                    if len(line) > 5 and len(line) < 100 and not line.lower().startswith(("abstract", "keywords", "the eurocall review")):
                        title = line
                        break
            
            # Extract text from all pages and analyze for headings
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get text with formatting information
                blocks = page.get_text("dict")
                
                for block in blocks.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line.get("spans", []):
                                text = span.get("text", "").strip()
                                font_size = span.get("size", 0)
                                font_flags = span.get("flags", 0)
                                
                                if self._is_heading(text, font_size, font_flags):
                                    level = self._determine_heading_level(text, font_size, font_flags)
                                    outline.append({
                                        "level": level,
                                        "text": text,
                                        "page": page_num + 1
                                    })
            
            # Also check for bookmarks/outline in PDF
            toc = doc.get_toc()
            for item in toc:
                level_num, heading_text, page_num = item
                level = f"H{min(level_num, 3)}"  # Cap at H3
                outline.append({
                    "level": level,
                    "text": heading_text.strip(),
                    "page": page_num
                })
        
        finally:
            doc.close()
        
        # Remove duplicates and sort by page
        outline = self._clean_outline(outline)
        
        return {
            "title": title or "Untitled Document",
            "outline": outline
        }
    
    def extract_outline_pdfplumber(self, pdf_path: str) -> Dict[str, Any]:
        """Extract outline using pdfplumber (fallback method)"""
        outline = []
        title = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            # Try to extract title from first page
            if pdf.pages:
                first_page_text = pdf.pages[0].extract_text()
                if first_page_text:
                    lines = first_page_text.split("\n")
                    for line in lines[:10]:
                        line = line.strip()
                        if len(line) > 5 and len(line) < 100 and not line.lower().startswith(("abstract", "keywords", "the eurocall review")):
                            title = line
                            break
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    lines = text.split("\n")
                    for line in lines:
                        line = line.strip()
                        if self._is_heading_text_only(line):
                            level = self._determine_heading_level_text_only(line)
                            outline.append({
                                "level": level,
                                "text": line,
                                "page": page_num + 1
                            })
        
        outline = self._clean_outline(outline)
        
        return {
            "title": title or "Untitled Document",
            "outline": outline
        }
    
    def _is_heading(self, text: str, font_size: float, font_flags: int) -> bool:
        """Determine if text is likely a heading based on formatting"""
        if not text or len(text.strip()) < self.min_heading_length or len(text.strip()) > self.max_heading_length:
            return False
        
        text = text.strip()
        
        # Filter out common non-heading text that might be bold/large
        if text.lower().startswith(("abstract", "keywords", "the eurocall review", "page")) or text.isdigit() or text.isspace() or len(text) < 5:
            return False

        # Check for common heading patterns
        for pattern in self.heading_patterns:
            if re.match(pattern, text):
                return True
        
        # Check font formatting (bold, larger size)
        is_bold = font_flags & 2**4  # Bold flag
        
        # Heuristics for headings
        if is_bold and font_size >= self.min_font_size_for_heading:
            return True
        
        # Consider lines that are significantly larger than body text as potential headings
        if font_size >= self.font_size_thresholds["H2"] and len(text) < 80:
            return True
        
        return False
    
    def _is_heading_text_only(self, text: str) -> bool:
        """Determine if text is likely a heading based on text patterns only"""
        if not text or len(text.strip()) < self.min_heading_length or len(text.strip()) > self.max_heading_length:
            return False
        
        text = text.strip()
        
        # Filter out common non-heading text
        if text.lower().startswith(("abstract", "keywords", "the eurocall review", "page")) or text.isdigit() or text.isspace() or len(text) < 5:
            return False

        # Check for common heading patterns
        for pattern in self.heading_patterns:
            if re.match(pattern, text):
                return True
        
        # Additional heuristics for text-only detection
        if len(text) < 80 and text.isupper(): # All caps and short
            return True
        
        return False
    
    def _determine_heading_level(self, text: str, font_size: float, font_flags: int) -> str:
        """Determine heading level based on text and formatting"""
        # Prioritize numbered patterns for academic papers
        if re.match(r"^\d+\.\d+\.\d+\s+", text):
            return "H3"
        elif re.match(r"^\d+\.\d+\s+", text):
            return "H2"
        elif re.match(r"^\d+\.\s+", text):
            return "H1"
        
        # Check for common academic section titles
        if re.match(r"^(Abstract|Introduction|Literature Review|Method|Methods|Results|Findings|Discussion|Conclusion|Conclusions|References)$", text, re.IGNORECASE):
            return "H1"

        # Check for chapter/section keywords
        if re.match(r"^(Chapter|CHAPTER)", text):
            return "H1"
        elif re.match(r"^(Section|SECTION)", text):
            return "H2"
        
        # Use font size as fallback for non-numbered headings
        if font_size >= self.font_size_thresholds["H1"]:
            return "H1"
        elif font_size >= self.font_size_thresholds["H2"]:
            return "H2"
        else:
            return "H3"
    
    def _determine_heading_level_text_only(self, text: str) -> str:
        """Determine heading level based on text patterns only"""
        # Prioritize numbered patterns
        if re.match(r"^\d+\.\d+\.\d+\s+", text):
            return "H3"
        elif re.match(r"^\d+\.\d+\s+", text):
            return "H2"
        elif re.match(r"^\d+\.\s+", text):
            return "H1"
        
        # Check for common academic section titles
        if re.match(r"^(Abstract|Introduction|Literature Review|Method|Methods|Results|Findings|Discussion|Conclusion|Conclusions|References)$", text, re.IGNORECASE):
            return "H1"

        # Check for keywords
        if re.match(r"^(Chapter|CHAPTER)", text):
            return "H1"
        elif re.match(r"^(Section|SECTION)", text):
            return "H2"
        
        # Default based on text characteristics
        if text.isupper() and len(text) < 50: # All caps and short
            return "H1"
        elif len(text) < 80: # Shorter lines are more likely to be headings
            return "H2"
        else:
            return "H3"
    
    def _clean_outline(self, outline: List[Dict]) -> List[Dict]:
        """Remove duplicates and clean up outline"""
        seen = set()
        cleaned = []
        
        for item in outline:
            # Create a key for deduplication (case-insensitive text and page)
            key = (item["text"].lower(), item["page"])
            if key not in seen:
                seen.add(key)
                cleaned.append(item)
        
        # Sort by page number and then by text length (shorter headings first)
        cleaned.sort(key=lambda x: (x["page"], len(x["text"])))
        
        return cleaned
    
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """Main method to extract outline from PDF"""
        try:
            # Try PyMuPDF first (more reliable for formatting)
            result = self.extract_outline_pymupdf(pdf_path)
            
            # If PyMuPDF yields no outline, try pdfplumber
            if not result["outline"]:
                result = self.extract_outline_pdfplumber(pdf_path)
            
            return result
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}", file=sys.stderr)
            return {
                "title": "Error Processing Document",
                "outline": []
            }


def process_pdf_file(input_path: str, output_path: str):
    """Process a single PDF file and save the outline as JSON"""
    extractor = PDFOutlineExtractor()
    result = extractor.extract_outline(input_path)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Processed: {input_path} -> {output_path}")


def main():
    """Main function to process all PDFs in input directory"""
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all PDF files in input directory
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    for pdf_file in pdf_files:
        output_file = output_dir / f"{pdf_file.stem}.json"
        process_pdf_file(str(pdf_file), str(output_file))
    
    print(f"Processed {len(pdf_files)} PDF files")


if __name__ == "__main__":
    main()


