import logging
from typing import Optional
from schemas.debitnote_schema import DebitNoteSchema
from extraction.extractor_utils import OllamaExtractionUtils

logger = logging.getLogger(__name__)


class DebitNoteExtractor:
    """Debit note extractor using your exact field specifications"""

    def __init__(self):
        self.utils = OllamaExtractionUtils()

    def extract(self, text: str) -> Optional[DebitNoteSchema]:
        """Extract debit note data matching your schema exactly"""

        additional_instructions = """
DEBIT NOTE EXTRACTION GUIDELINES:
- Extract debit_note_number, debit_date
- Get party information: vendor_name, vendor_address
- Find reference information: linked_invoice_id (if mentioned)
- Extract financial details: debit_amount, cgst_amount, sgst_amount, igst_amount
- Get additional details: reason, reference_number, status, company_name

IMPORTANT:
- Dates in DD-MM-YYYY format
- Numbers without currency symbols or commas
- Only extract linked_invoice_id if explicitly mentioned in document
- Use exact field names from schema
"""

        try:
            result = self.utils.extract_with_retry(
                text=text,
                schema=DebitNoteSchema,
                document_type="debit_note",
                additional_instructions=additional_instructions
            )

            if result:
                result = self._post_process_debit_note(result)
                logger.info("Debit note extraction completed successfully")
                return result
            else:
                logger.error("Debit note extraction failed")
                return None

        except Exception as e:
            logger.error(f"Debit note extraction error: {str(e)}")
            return None

    def _post_process_debit_note(self, debit_note: DebitNoteSchema) -> DebitNoteSchema:
        """Post-process extracted debit note data"""

        # Normalize date
        if debit_note.debit_date:
            debit_note.debit_date = self._normalize_date(debit_note.debit_date)

        # Clean numeric values
        numeric_fields = [
            'debit_amount', 'cgst_amount', 'sgst_amount', 'igst_amount'
        ]

        for field in numeric_fields:
            value = getattr(debit_note, field, None)
            if value is not None:
                setattr(debit_note, field, self._safe_float_conversion(value))

        debit_note.document_type = "debit_note"
        return debit_note

    def _safe_float_conversion(self, value) -> Optional[float]:
        """Safely convert value to float"""
        if value is None:
            return None

        try:
            if isinstance(value, (int, float)):
                return float(value)

            if isinstance(value, str):
                cleaned = value.replace('₹', '').replace('Rs', '').replace(',', '').strip()
                if cleaned and cleaned not in ['', '-', 'N/A', 'null']:
                    return float(cleaned)

            return None
        except (ValueError, TypeError):
            return None

    def _normalize_date(self, date_str: str) -> Optional[str]:
        """Normalize date string to DD-MM-YYYY format"""
        if not date_str:
            return None

        try:
            from datetime import datetime
            formats = [
                '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y',
                '%B %d, %Y', '%d %B %Y', '%b %d, %Y', '%d %b %Y'
            ]

            for fmt in formats:
                try:
                    dt = datetime.strptime(str(date_str).strip(), fmt)
                    return dt.strftime('%d-%m-%Y')
                except ValueError:
                    continue

            return str(date_str)
        except Exception:
            return str(date_str)
