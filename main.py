import os
import json
import logging
from pathlib import Path

from config import config
from loaders.document_loader import DocumentLoader
from classification.classifier import DocumentClassifier

# Import extractors
from extraction.invoice_extractor import InvoiceExtractor
from extraction.payroll_extractor import PayrollExtractor
from extraction.receipt_extractor import ReceiptExtractor
from extraction.bank_extractor import BankExtractor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


class DocumentPipeline:
    """Main pipeline for document classification and extraction"""

    def __init__(self):
        self.loader = DocumentLoader()
        self.classifier = DocumentClassifier()

        # Register extractors
        self.extractors = {
            "invoice": InvoiceExtractor(),
            "payroll": PayrollExtractor(),
            "receipt": ReceiptExtractor(),
            "bank_statement": BankExtractor(),
        }

    def process_document(self, file_path: Path):
        """Process a single document end-to-end"""
        try:
            logger.info(f"📂 Processing: {file_path.name}")

            # Step 1: Load document text
            text = self.loader.get_document_text(file_path)
            # print(text)

            # Step 2: Classify document
            doc_type = self.classifier.classify(text)
            if not doc_type:
                logger.error(f"❌ Could not classify document: {file_path.name}")
                return
            print(doc_type)

            # Step 3: Extract with correct extractor
            # extractor = self.extractors.get(doc_type)
            # if not extractor:
            #     logger.error(f"❌ No extractor available for type: {doc_type}")
            #     return
            #
            # schema_obj = extractor.extract(text)
            # if not schema_obj:
            #     logger.error(f"❌ Extraction failed for {file_path.name}")
            #     return

            # Step 4: Add metadata
            # schema_obj.source_file = file_path.name

            # Step 5: Save output as JSON
            # output_path = config.OUTPUT_JSON_DIR / f"{file_path.stem}.json"
            # with open(output_path, "w", encoding="utf-8") as f:
            #     json.dump(schema_obj, f, indent=4, ensure_ascii=False)
            #
            # logger.info(f"✅ Saved extracted JSON → {output_path}")

        except Exception as e:
            logger.error(f"⚠️ Pipeline error for {file_path.name}: {str(e)}")

    def run(self):
        """Run pipeline on all documents in input_docs"""
        files = list(config.INPUT_DOCS_DIR.glob("*"))

        if not files:
            logger.warning("⚠️ No input documents found in input_docs/")
            return

        for file in files:
            self.process_document(file)


if __name__ == "__main__":
    pipeline = DocumentPipeline()
    pipeline.run()
