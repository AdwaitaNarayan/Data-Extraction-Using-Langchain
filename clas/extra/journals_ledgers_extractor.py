from langchain_ollama import ChatOllama
from langchain_core.output_parsers.json import JsonOutputParser
import json


class JournalsLedgersExtractor:
    """
    Extractor for Journals & Ledgers:
      - General Journal
      - General Ledger
      - Cash Book
      - Petty Cash Book
      - Accounts Payable Ledger
      - Accounts Receivable Ledger
    """

    def __init__(self, model="llama2:latest", base_url="http://localhost:11434"):
        self.llm = ChatOllama(model=model, base_url=base_url)
        self.parser = JsonOutputParser()

    def _extract(self, text: str, schema: dict, instruction: str) -> dict:
        """Generic extraction logic"""
        prompt = f"""
        You are an expert accounting document data extractor.
        Extract ONLY the following fields as valid JSON, following the schema below.

        Schema:
        {json.dumps(schema, indent=2)}

        Rules:
        - Do not include any text outside JSON.
        - Use null for missing or unavailable fields.
        - Keep field names exactly as in schema.
        - Extract numeric values as numbers.

        {instruction}

        Document:
        {text}
        """
        response = self.llm.invoke(prompt)
        return self.parser.parse(response.content)

    # --------------------------------------------------------------------------
    def extract_general_journal(self, text: str):
        schema = {
            "journal_id": "string",
            "date_of_entry": "string",
            "reference_number": "string",
            "description": "string",
            "entries": [
                {
                    "account_name": "string",
                    "account_code": "string",
                    "debit_amount": "number",
                    "credit_amount": "number",
                    "ledger_folio": "string",
                    "currency": "string",
                    "department": "string",
                    "cost_center": "string"
                }
            ],
            "prepared_by": "string",
            "approved_by": "string",
            "remarks": "string",
            "supporting_document_reference": "string"
        }

        return self._extract(text, schema, "Extract all fields for a General Journal document.")

    # --------------------------------------------------------------------------
    def extract_general_ledger(self, text: str):
        schema = {
            "ledger_account_name": "string",
            "account_code": "string",
            "date": "string",
            "particulars": "string",
            "reference_number": "string",
            "debit_amount": "number",
            "credit_amount": "number",
            "balance_brought_forward": "number",
            "running_balance": "number",
            "business_unit": "string",
            "cost_center": "string",
            "currency": "string",
            "exchange_rate": "number",
            "posting_period": "string",
            "fiscal_year": "string",
            "account_type": "string"
        }

        return self._extract(text, schema, "Extract all fields for a General Ledger document.")

    # --------------------------------------------------------------------------
    def extract_cash_book(self, text: str):
        schema = {
            "date": "string",
            "voucher_number": "string",
            "receipt_number": "string",
            "particulars": "string",
            "payer_payee_details": "string",
            "description": "string",
            "reference_document_id": "string",
            "cash_received": "number",
            "cash_paid": "number",
            "balance_after_transaction": "number",
            "mode_of_payment": "string",
            "authorized_by": "string",
            "verified_by": "string",
            "remarks": "string"
        }

        return self._extract(text, schema, "Extract all fields for a Cash Book document.")

    # --------------------------------------------------------------------------
    def extract_petty_cash_book(self, text: str):
        schema = {
            "date": "string",
            "voucher_number": "string",
            "expense_category": "string",
            "description": "string",
            "amount_paid": "number",
            "total_daily_expenses": "number",
            "total_monthly_expenses": "number",
            "reimbursement_amount_received": "number",
            "closing_balance": "number",
            "prepared_by": "string",
            "checked_by": "string",
            "receiver_signature": "string"
        }

        return self._extract(text, schema, "Extract all fields for a Petty Cash Book document.")

    # --------------------------------------------------------------------------
    def extract_accounts_payable_ledger(self, text: str):
        schema = {
            "supplier_name": "string",
            "supplier_id": "string",
            "account_code": "string",
            "invoice_number": "string",
            "invoice_date": "string",
            "purchase_order_number": "string",
            "description_of_purchase": "string",
            "amount_before_tax": "number",
            "tax": {
                "cgst": "number",
                "sgst": "number",
                "igst": "number",
                "vat": "number"
            },
            "total_payable_amount": "number",
            "payments_made": "number",
            "credits_applied": "number",
            "balance_outstanding": "number",
            "due_date": "string",
            "terms_of_payment": "string",
            "currency": "string",
            "exchange_rate": "number",
            "aging": {
                "current": "number",
                "30_days": "number",
                "60_days": "number",
                "90_days": "number",
                "above_90_days": "number"
            },
            "contact_person": "string",
            "email": "string",
            "phone": "string"
        }

        return self._extract(text, schema, "Extract all fields for an Accounts Payable Ledger document.")

    # --------------------------------------------------------------------------
    def extract_accounts_receivable_ledger(self, text: str):
        schema = {
            "customer_name": "string",
            "customer_id": "string",
            "account_code": "string",
            "invoice_number": "string",
            "invoice_date": "string",
            "sales_order_reference": "string",
            "delivery_note_reference": "string",
            "description_of_goods_services": "string",
            "tax_details": {
                "cgst": "number",
                "sgst": "number",
                "igst": "number"
            },
            "total_receivable_amount": "number",
            "payments_received": "number",
            "adjustments": "number",
            "credit_notes_issued": "number",
            "outstanding_balance": "number",
            "due_date": "string",
            "collection_status": "string",
            "ageing_bucket": {
                "current": "number",
                "30_days": "number",
                "60_days": "number",
                "90_days": "number",
                "above_90_days": "number"
            },
            "remarks": "string",
            "contact_details": "string"
        }

        return self._extract(text, schema, "Extract all fields for an Accounts Receivable Ledger document.")
