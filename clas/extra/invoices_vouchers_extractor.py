from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser

import json

class InvoicesVouchersExtractor:
    def __init__(self, model="llama2:latest", base_url="http://localhost:11434"):
        self.llm = ChatOllama(model=model, base_url=base_url)

    def extract_sales_invoice(self, text: str):
        """Extract structured fields for a Sales Invoice"""
        schema = {
            "invoice_number": "string",
            "invoice_date": "string",
            "customer_name": "string",
            "customer_gstin": "string",
            "items": [
                {
                    "description": "string",
                    "hsn_code": "string",
                    "quantity": "number",
                    "unit_price": "number",
                    "amount": "number"
                }
            ],
            "subtotal": "number",
            "tax_total": "number",
            "grand_total": "number"
        }

        prompt = f"""
        You are a strict document information extractor.
        Extract ONLY the following fields as JSON:
        {json.dumps(schema, indent=2)}

        Document:
        {text}
        """

        response = self.llm.invoke(prompt)
        parser = JsonOutputParser()
        return parser.parse(response.content)

    def extract_payroll(self, text: str):
        """Extract structured fields for a Payroll"""
        schema = {
            "employee_id": "string",
            "employee_name": "string",
            "designation": "string",
            "department": "string",
            "basic_pay": "number",
            "hra": "number",
            "gross_salary": "number",
            "deductions": "number",
            "net_pay": "number"
        }

        prompt = f"""
        You are an expert payroll document extractor.
        Extract details according to the schema below in valid JSON:
        {json.dumps(schema, indent=2)}

        Document:
        {text}
        """

        response = self.llm.invoke(prompt)
        parser = JsonOutputParser()
        return parser.parse(response.content)

# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers.json import JsonOutputParser
# import json
#
#
# class InvoicesVouchersExtractor:
#     """
#     Extractor for all document types under 'Invoices & Vouchers' category:
#       - Sales Invoice
#       - Purchase Invoice
#       - Receipt
#       - Payment Voucher
#       - Bank Statement
#       - Payroll
#       - Expense Voucher
#       - Credit Note
#       - Debit Note
#     """
#
#     def __init__(self, model="llama2:latest", base_url="http://localhost:11434"):
#         self.llm = ChatOllama(model=model, base_url=base_url)
#         self.parser = JsonOutputParser()
#
#     # --------------------------------------------------------------------------
#     def _extract(self, text: str, schema: dict, instruction: str) -> dict:
#         """Generic extractor for a document based on given schema and prompt"""
#         prompt = f"""
#         You are an expert document information extractor.
#         Extract ONLY the following fields in valid JSON format.
#         Use the schema below as guidance for structure and field names.
#
#         Schema:
#         {json.dumps(schema, indent=2)}
#
#         Rules:
#         - Ensure JSON keys match exactly.
#         - If a field is missing, return null.
#         - Extract numeric values as numbers, not strings.
#
#         {instruction}
#
#         Document:
#         {text}
#         """
#         response = self.llm.invoke(prompt)
#
#         # Handle text content safely
#         if hasattr(response, "content"):
#             raw_output = response.content
#         elif isinstance(response, str):
#             raw_output = response
#         elif hasattr(response, "message") and hasattr(response.message, "content"):
#             raw_output = response.message.content
#         else:
#             raw_output = str(response)
#
#         try:
#             return self.parser.parse(raw_output)
#         except Exception:
#             # If parsing fails, just return the raw text for debugging
#             return {"raw_output": raw_output}
#
#         # return self.parser.parse(response.content)
#
#     # --------------------------------------------------------------------------
#     def extract_sales_invoice(self, text: str):
#         schema = {
#             "seller": {
#                 "name": "string",
#                 "address": "string",
#                 "gstin": "string",
#                 "email": "string",
#                 "phone": "string"
#             },
#             "buyer": {
#                 "name": "string",
#                 "address": "string",
#                 "gstin": "string",
#                 "email": "string",
#                 "phone": "string"
#             },
#             "invoice_number": "string",
#             "invoice_date": "string",
#             "due_date": "string",
#             "purchase_order_number": "string",
#             "items": [
#                 {
#                     "product_name": "string",
#                     "description": "string",
#                     "quantity": "number",
#                     "unit_price": "number",
#                     "discount": "number",
#                     "tax_rate": "number",
#                     "tax_type": "string",
#                     "line_total": "number"
#                 }
#             ],
#             "subtotal": "number",
#             "total_tax_amount": "number",
#             "shipping_charge": "number",
#             "total_amount": "number",
#             "payment_terms": {
#                 "due_date": "string",
#                 "method": "string"
#             },
#             "notes": "string",
#             "authorized_signatory": "string"
#         }
#
#         return self._extract(text, schema, "Extract all fields related to a Sales Invoice.")
#
#     # --------------------------------------------------------------------------
#     def extract_purchase_invoice(self, text: str):
#         schema = {
#             "supplier": {
#                 "name": "string",
#                 "address": "string",
#                 "gstin": "string",
#                 "email": "string",
#                 "phone": "string"
#             },
#             "buyer": {
#                 "name": "string",
#                 "address": "string",
#                 "gstin": "string"
#             },
#             "invoice_number": "string",
#             "invoice_date": "string",
#             "due_date": "string",
#             "grn_or_po_number": "string",
#             "items": [
#                 {
#                     "description": "string",
#                     "quantity": "number",
#                     "unit_cost": "number",
#                     "tax_rate": "number",
#                     "tax_type": "string"
#                 }
#             ],
#             "subtotal": "number",
#             "total_tax": "number",
#             "total_payable_amount": "number",
#             "payment_reference": "string",
#             "ledger_accounts": {
#                 "expense_account": "string",
#                 "credit_account": "string"
#             },
#             "approval_status": "string",
#             "internal_reference_notes": "string"
#         }
#
#         return self._extract(text, schema, "Extract all fields related to a Purchase Invoice.")
#
#     # --------------------------------------------------------------------------
#     def extract_receipt(self, text: str):
#         schema = {
#             "receipt_number": "string",
#             "receipt_date": "string",
#             "payer": {
#                 "name": "string",
#                 "address": "string",
#                 "contact_info": "string"
#             },
#             "payee": {
#                 "name": "string",
#                 "address": "string",
#                 "contact_info": "string"
#             },
#             "payment_mode": "string",
#             "reference_id": "string",
#             "received_amount": "number",
#             "tax_amount": "number",
#             "purpose": "string",
#             "balance_due": "number",
#             "authorized_signature": "string"
#         }
#
#         return self._extract(text, schema, "Extract all fields related to a Receipt.")
#
#     # --------------------------------------------------------------------------
#     def extract_payment_voucher(self, text: str):
#         schema = {
#             "voucher_number": "string",
#             "date": "string",
#             "paid_to": {
#                 "name": "string",
#                 "details": "string"
#             },
#             "purpose": "string",
#             "payment_mode": "string",
#             "account_details": {
#                 "credited_account": "string",
#                 "debited_account": "string"
#             },
#             "tax_withheld": "number",
#             "total_payment_amount": "number",
#             "approval_authority": "string",
#             "supporting_reference": "string"
#         }
#
#         return self._extract(text, schema, "Extract all fields related to a Payment Voucher.")
#
#     # --------------------------------------------------------------------------
#     def extract_bank_statement(self, text: str):
#         schema = {
#             "bank_name": "string",
#             "branch_address": "string",
#             "contact_info": "string",
#             "account_holder": {
#                 "name": "string",
#                 "address": "string",
#                 "account_number": "string"
#             },
#             "statement_period": {
#                 "start_date": "string",
#                 "end_date": "string"
#             },
#             "opening_balance": "number",
#             "closing_balance": "number",
#             "transactions": [
#                 {
#                     "date": "string",
#                     "description": "string",
#                     "debit": "number",
#                     "credit": "number",
#                     "balance": "number",
#                     "reference_id": "string",
#                     "charges": "number"
#                 }
#             ]
#         }
#
#         return self._extract(text, schema, "Extract all fields related to a Bank Statement.")
#
#     # --------------------------------------------------------------------------
#     def extract_payroll(self, text: str):
#         schema = {
#             "employee": {
#                 "id": "string",
#                 "name": "string",
#                 "designation": "string",
#                 "department": "string"
#             },
#             "period": "string",
#             "pay_date": "string",
#             "basic_pay": "number",
#             "hra": "number",
#             "allowances": "number",
#             "deductions": "number",
#             "gross_salary": "number",
#             "net_salary": "number",
#             "tax_deductions": {
#                 "tds": "number",
#                 "pf": "number",
#                 "esi": "number",
#                 "other": "number"
#             },
#             "bank_details": {
#                 "account_number": "string",
#                 "ifsc_code": "string"
#             },
#             "employer": {
#                 "name": "string",
#                 "address": "string",
#                 "gst_or_tan": "string"
#             },
#             "pay_slip_number": "string",
#             "attendance_days": "number",
#             "overtime_hours": "number",
#             "leave_deductions": "number",
#             "payment_mode": "string"
#         }
#
#         return self._extract(text, schema, "Extract all fields related to a Payroll document.")
#
#     # --------------------------------------------------------------------------
#     def extract_expense_voucher(self, text: str):
#         schema = {
#             "voucher_number": "string",
#             "date": "string",
#             "employee_name": "string",
#             "department": "string",
#             "project": "string",
#             "expense_category": "string",
#             "description": "string",
#             "amount": "number",
#             "currency": "string",
#             "supporting_bills": "string",
#             "approved_by": "string",
#             "payment_mode": "string",
#             "payment_date": "string",
#             "total_reimbursable_amount": "number"
#         }
#
#         return self._extract(text, schema, "Extract all fields related to an Expense Voucher.")
#
#     # --------------------------------------------------------------------------
#     def extract_credit_note(self, text: str):
#         schema = {
#             "credit_note_number": "string",
#             "date": "string",
#             "original_invoice": {
#                 "number": "string",
#                 "date": "string"
#             },
#             "customer": {
#                 "name": "string",
#                 "address": "string",
#                 "gstin": "string"
#             },
#             "seller": {
#                 "name": "string",
#                 "address": "string",
#                 "gstin": "string"
#             },
#             "items": [
#                 {
#                     "description": "string",
#                     "quantity": "number",
#                     "unit_price": "number",
#                     "tax_rate": "number",
#                     "amount": "number"
#                 }
#             ],
#             "reason_for_credit": "string",
#             "total_before_tax": "number",
#             "total_tax": "number",
#             "total_credit_amount": "number",
#             "authorized_signature": "string",
#             "reference_ledger_entry": "string"
#         }
#
#         return self._extract(text, schema, "Extract all fields related to a Credit Note.")
#
#     # --------------------------------------------------------------------------
#     def extract_debit_note(self, text: str):
#         schema = {
#             "debit_note_number": "string",
#             "date": "string",
#             "original_invoice_reference": "string",
#             "supplier": {
#                 "name": "string",
#                 "address": "string",
#                 "gstin": "string"
#             },
#             "buyer": {
#                 "name": "string",
#                 "address": "string",
#                 "gstin": "string"
#             },
#             "items": [
#                 {
#                     "description": "string",
#                     "quantity": "number",
#                     "rate": "number",
#                     "tax_rate": "number",
#                     "amount": "number"
#                 }
#             ],
#             "total_taxable_value": "number",
#             "total_tax": "number",
#             "total_debit_amount": "number",
#             "reason_for_debit": "string",
#             "remarks": "string",
#             "approved_by": "string",
#             "issued_by": "string"
#         }
#
#         return self._extract(text, schema, "Extract all fields related to a Debit Note.")
