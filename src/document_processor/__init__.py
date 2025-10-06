"""
Document processor package
"""
from .pdf_extractor import PDFExtractor
from .docx_extractor import DOCXExtractor
from .doc_extractor import DOCExtractor
from .text_extractor import TextExtractor

__all__ = ['PDFExtractor', 'DOCXExtractor', 'DOCExtractor', 'TextExtractor']
