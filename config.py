from typing import Dict, Any, List
import os
from pathlib import Path


class Config:
    # Ollama Configuration
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODELS = {
        "classification": "llama2:latest",
        "extraction": "llama2:latest"
    }

    # Model Parameters
    TEMPERATURE = 0.1
    TOP_P = 0.9
    TOP_K = 40

    # Document Types
    DOCUMENT_TYPES = [
        "invoice",
        "bank_statement",
        "payroll",
        "receipt",
        "debit_note",
        "credit_note"
    ]

    # Paths
    BASE_DIR = Path(__file__).parent
    INPUT_DOCS_DIR = BASE_DIR / "input_docs"
    OUTPUT_JSON_DIR = BASE_DIR / "output_json"

    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1

    # OCR Settings
    TESSERACT_CONFIG = "--oem 3 --psm 6"


config = Config()
