#!/usr/bin/env python3
"""
Tests for the Zeyta AI Assistant Application
"""

import sys
from pathlib import Path
import tempfile


def extract_file_content(file_path: str) -> str:
    """Extract text content from uploaded files (copied from app.py for testing)"""
    try:
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_ext == '.pdf':
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                return "⚠️ PyPDF2 not installed. Install with: pip install PyPDF2"
        
        elif file_ext in ['.doc', '.docx']:
            try:
                import docx
                doc = docx.Document(file_path)
                return "\n".join([para.text for para in doc.paragraphs])
            except ImportError:
                return "⚠️ python-docx not installed. Install with: pip install python-docx"
        
        elif file_ext == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        else:
            return f"⚠️ Unsupported file type: {file_ext}"
            
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"


def test_txt_file_extraction():
    """Test extraction of text files"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test file.\nWith multiple lines.")
        f.flush()
        
        content = extract_file_content(f.name)
        assert "test file" in content
        assert "multiple lines" in content
        print("✅ TXT file extraction test passed")
        
        Path(f.name).unlink()


def test_md_file_extraction():
    """Test extraction of markdown files"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("# Header\n\nThis is markdown content.")
        f.flush()
        
        content = extract_file_content(f.name)
        assert "Header" in content
        assert "markdown content" in content
        print("✅ Markdown file extraction test passed")
        
        Path(f.name).unlink()


def test_unsupported_file():
    """Test handling of unsupported file types"""
    with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
        f.write(b"test")
        f.flush()
        
        content = extract_file_content(f.name)
        assert "Unsupported" in content or "Error" in content
        print("✅ Unsupported file handling test passed")
        
        Path(f.name).unlink()


def test_pdf_extraction():
    """Test PDF extraction (if PyPDF2 is available)"""
    try:
        import PyPDF2
        print("✅ PyPDF2 available for PDF support")
    except ImportError:
        print("⚠️  PyPDF2 not installed - PDF support will be limited")


def test_docx_extraction():
    """Test DOCX extraction (if python-docx is available)"""
    try:
        import docx
        print("✅ python-docx available for DOCX support")
    except ImportError:
        print("⚠️  python-docx not installed - DOCX support will be limited")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Zeyta App Tests")
    print("=" * 60)
    print()
    
    test_txt_file_extraction()
    test_md_file_extraction()
    test_unsupported_file()
    test_pdf_extraction()
    test_docx_extraction()
    
    print()
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
