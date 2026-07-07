import os
from pathlib import Path
from typing import List, Union
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from config import config


class DocumentLoader:
    """Document loader with OCR fallback for images and PDFs"""

    def __init__(self):
        self.supported_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}

    def get_document_text(self, file_path: Union[str, Path]) -> str:
        """Extract text from document and return as string"""
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

        print(f"📄 Loading document: {file_path.name}")

        if file_path.suffix.lower() == '.pdf':
            text = self._extract_pdf_text(file_path)
        else:
            text = self._extract_image_text(file_path)

        print(f"✅ Text extraction completed - {len(text)} characters")
        return text

    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF using PyPDF first, OCR fallback"""
        try:
            # Try PyPDFLoader first
            loader = PyPDFLoader(str(file_path))
            documents = loader.load()
            text = "\n".join([doc.page_content for doc in documents])

            if len(text.strip()) > 50:  # Has meaningful text
                print("✓ PDF text extracted directly")
                return text
            else:
                print("⚠️ PDF has minimal text, using OCR...")
                return self._pdf_ocr_fallback(file_path)

        except Exception as e:
            print(f"⚠️ PDF extraction failed, using OCR: {str(e)}")
            return self._pdf_ocr_fallback(file_path)

    def _pdf_ocr_fallback(self, file_path: Path) -> str:
        """OCR fallback for PDFs"""
        try:
            doc = fitz.open(str(file_path))
            full_text = ""

            for page_num in range(doc.page_count):
                page = doc[page_num]
                # Convert to high resolution image
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("png")

                # OCR the image
                image = Image.open(io.BytesIO(img_data))
                text = pytesseract.image_to_string(image, config=config.TESSERACT_CONFIG)
                full_text += f"\n--- Page {page_num + 1} ---\n{text}\n"

            doc.close()
            print(f"✓ OCR completed for {doc.page_count} pages")
            return full_text

        except Exception as e:
            raise Exception(f"OCR failed: {str(e)}")

    def _extract_image_text(self, file_path: Path) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, config=config.TESSERACT_CONFIG)
            print("✓ Image OCR completed")
            return text
        except Exception as e:
            raise Exception(f"Image OCR failed: {str(e)}")
