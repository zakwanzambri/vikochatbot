"""
PDF text extraction using PyMuPDF
"""
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List


class PDFExtractor:
    """Extract text from PDF files"""
    
    def __init__(self):
        self.supported_extension = '.pdf'
    
    def extract_text(self, file_path: str) -> Dict[str, any]:
        """
        Extract text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing:
                - text: Extracted text
                - pages: Number of pages
                - filename: Original filename
                - metadata: PDF metadata
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() != self.supported_extension:
            raise ValueError(f"Invalid file type. Expected {self.supported_extension}, got {path.suffix}")
        
        try:
            doc = fitz.open(file_path)
            text_parts = []
            
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                text_parts.append(page.get_text())
            
            full_text = "\n\n".join(text_parts)
            metadata = doc.metadata
            page_count = len(doc)
            
            doc.close()
            
            return {
                'text': full_text,
                'pages': page_count,
                'filename': path.name,
                'metadata': metadata,
                'file_type': 'pdf'
            }
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_by_page(self, file_path: str) -> List[Dict[str, any]]:
        """
        Extract text from a PDF file, page by page
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of dictionaries, one per page
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            doc = fitz.open(file_path)
            pages_data = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                pages_data.append({
                    'page_number': page_num + 1,
                    'text': page.get_text(),
                    'filename': path.name
                })
            
            doc.close()
            return pages_data
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
