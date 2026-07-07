from typing import Optional
from schemas.invoice_schema import InvoiceSchema
from extraction.extractor_utils import OllamaExtractionUtils


class InvoiceExtractor:
    """Invoice extractor using exact field specifications"""

    def __init__(self):
        self.utils = OllamaExtractionUtils()

    def extract(self, text: str) -> Optional[InvoiceSchema]:
        """Extract invoice data matching schema exactly"""

        additional_instructions = """
INVOICE EXTRACTION GUIDELINES:
- Extract invoice_number, invoice_date, due_date
- Get party details: name, type, GSTIN, address, email, phone
- Calculate amounts: base_amount, tax amounts (CGST/SGST/IGST rates and amounts), total_amount
- Find accounting info: debit_account, credit_account, description
- Extract reference_number, status, company_name, invoice_type, hsn_code
- For invoice_items: extract product_name, manufacturer_name, batch_number, HSN, quantity, MRP, discounts, tax details

IMPORTANT:
- Dates in DD-MM-YYYY format
- Numbers without currency symbols or commas
- Extract all line items if present
- Calculate tax amounts accurately
"""

        return self.utils.extract_with_retry(
            text=text,
            schema=InvoiceSchema,
            document_type="invoice",
            additional_instructions=additional_instructions
        )
