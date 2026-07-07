from typing import Optional
from schemas.receipt_schema import ReceiptSchema
from extraction.extractor_utils import OllamaExtractionUtils


class ReceiptExtractor:
    """Receipt extractor using exact field specifications"""

    def __init__(self):
        self.utils = OllamaExtractionUtils()

    def extract(self, text: str) -> Optional[ReceiptSchema]:
        """Extract receipt data matching schema exactly"""

        additional_instructions = """
RECEIPT EXTRACTION GUIDELINES:
- Extract receipt_number, receipt_date
- Get party information: party_name, party_address
- Find payment details: amount_paid, payment_method
- Extract bank details: bank_details, cheque_number, transaction_id
- Get financial details: subtotal, tax_amount, total_amount
- Find additional info: company_name, reference_number, status, remarks

IMPORTANT:
- Dates in DD-MM-YYYY format
- Numbers without currency symbols or commas
- Extract linked invoice number if mentioned
- Payment methods: cash, cheque, online, card, etc.
"""

        return self.utils.extract_with_retry(
            text=text,
            schema=ReceiptSchema,
            document_type="receipt",
            additional_instructions=additional_instructions
        )
