from langchain_ollama import ChatOllama
from langchain_core.output_parsers.json import JsonOutputParser
import json


class TaxComplianceExtractor:
    """
    Extractor for Tax & Compliance documents:
      - Tax Return
      - Audit Report
      - Annual Report
      - GST Compliance Reports
      - Company Incorporation Docs
      - Board Resolutions
    """

    def __init__(self, model="llama2:latest", base_url="http://localhost:11434"):
        self.llm = ChatOllama(model=model, base_url=base_url)
        self.parser = JsonOutputParser()

    def _extract(self, text: str, schema: dict, instruction: str) -> dict:
        """Generic LLM-based extraction utility"""
        prompt = f"""
        You are an expert compliance and tax document extractor.
        Extract ONLY the following fields in valid JSON format based on the schema below.

        Schema:
        {json.dumps(schema, indent=2)}

        Rules:
        - Follow field names exactly.
        - Use null for missing or unavailable values.
        - Maintain nested structure as shown.
        - Extract numeric values as numbers.
        - Return ONLY JSON.

        {instruction}

        Document:
        {text}
        """
        response = self.llm.invoke(prompt)
        return self.parser.parse(response.content)

    # --------------------------------------------------------------------------
    def extract_tax_return(self, text: str):
        schema = {
            "form_type": "string",
            "assessment_year": "string",
            "financial_year": "string",
            "pan_or_tin": "string",
            "aadhaar_or_business_registration": "string",
            "taxpayer": {
                "name": "string",
                "address": "string",
                "contact_number": "string",
                "email": "string"
            },
            "nature_of_business": "string",
            "filing_status": "string",
            "residential_status": "string",
            "sources_of_income": {
                "salary": "number",
                "business_income": "number",
                "capital_gains": "number",
                "house_property": "number",
                "other_sources": "number"
            },
            "gross_total_income": "number",
            "deductions": "string",
            "net_taxable_income": "number",
            "tax_computation": {
                "tax_payable": "number",
                "tds": "number",
                "advance_tax": "number",
                "interest_234B_234C": "number"
            },
            "total_tax_paid_or_refund": "number",
            "bank_details": {
                "bank_name": "string",
                "account_number": "string",
                "ifsc_code": "string"
            },
            "verification_section": {
                "verified_by": "string",
                "designation": "string",
                "signature": "string"
            },
            "auditor_details": {
                "name": "string",
                "firm_name": "string",
                "membership_number": "string"
            },
            "attachments": "string"
        }
        return self._extract(text, schema, "Extract all fields related to a Tax Return document.")

    # --------------------------------------------------------------------------
    def extract_audit_report(self, text: str):
        schema = {
            "company": {
                "name": "string",
                "cin": "string",
                "registered_address": "string"
            },
            "auditor": {
                "firm_name": "string",
                "registration_number": "string",
                "address": "string"
            },
            "audit_period": "string",
            "financial_year": "string",
            "audit_type": "string",
            "auditor_opinion": "string",
            "basis_for_opinion": "string",
            "key_audit_matters": "string",
            "management_responsibility": "string",
            "auditor_responsibility": "string",
            "comments_on_internal_controls": "string",
            "annexures": {
                "balance_sheet_abstract": "string",
                "profit_loss_summary": "string",
                "caro_checklist": "string"
            },
            "signature": "string",
            "membership_number": "string",
            "date": "string",
            "place": "string"
        }
        return self._extract(text, schema, "Extract all fields related to an Audit Report document.")

    # --------------------------------------------------------------------------
    def extract_annual_report(self, text: str):
        schema = {
            "corporate_information": {
                "cin": "string",
                "registered_office": "string",
                "contact_details": "string"
            },
            "chairman_ceo_message": "string",
            "directors_report": "string",
            "management_discussion_analysis": "string",
            "corporate_governance_report": "string",
            "shareholding_pattern": "string",
            "independent_auditor_report": "string",
            "financial_statements": {
                "balance_sheet": "string",
                "profit_and_loss": "string",
                "cash_flow": "string"
            },
            "notes_to_accounts": "string",
            "esg_csr_disclosures": "string",
            "subsidiary_information": "string",
            "board_meeting_attendance": "string",
            "committees_overview": "string",
            "secretarial_auditor_report": "string",
            "declaration_of_compliance": "string"
        }
        return self._extract(text, schema, "Extract all fields related to an Annual Report document.")

    # --------------------------------------------------------------------------
    def extract_gst_compliance_reports(self, text: str):
        schema = {
            "gstin": "string",
            "legal_name": "string",
            "trade_name": "string",
            "reporting_period": "string",
            "return_type": "string",
            "output_tax_details": {
                "taxable_supplies": "number",
                "exempt_nil_rated": "number",
                "exports": "number"
            },
            "input_tax_credit": {
                "eligible_itc": "number",
                "ineligible_itc": "number",
                "itc_reversal": "number"
            },
            "tax_summary": {
                "cgst": "number",
                "sgst": "number",
                "igst": "number",
                "cess": "number"
            },
            "transaction_summary": {
                "b2b": "number",
                "b2c": "number",
                "sez": "number"
            },
            "payment_summary": {
                "challan_number": "string",
                "date": "string",
                "amount": "number"
            },
            "late_fees": "number",
            "interest": "number",
            "penalties": "number",
            "digital_signature": "string",
            "filing_acknowledgement": "string"
        }
        return self._extract(text, schema, "Extract all fields related to GST Compliance Reports.")

    # --------------------------------------------------------------------------
    def extract_company_incorporation_docs(self, text: str):
        schema = {
            "form_type": "string",
            "company_name": "string",
            "cin": "string",
            "company_type": "string",
            "registered_office_address": "string",
            "director_details": [
                {
                    "din": "string",
                    "name": "string",
                    "pan": "string",
                    "address": "string",
                    "nationality": "string"
                }
            ],
            "shareholder_details": [
                {
                    "name": "string",
                    "shares_held": "number",
                    "percentage_ownership": "number"
                }
            ],
            "capital_structure": {
                "authorized_capital": "number",
                "subscribed_capital": "number",
                "paid_up_capital": "number"
            },
            "main_objects_of_business": "string",
            "declaration_by_professional": {
                "name": "string",
                "designation": "string"
            },
            "digital_signatures": {
                "subscribers": "string",
                "professionals": "string"
            },
            "certificate_of_incorporation": {
                "issue_date": "string",
                "issued_by": "string"
            }
        }
        return self._extract(text, schema, "Extract all fields related to Company Incorporation Documents.")

    # --------------------------------------------------------------------------
    def extract_board_resolutions(self, text: str):
        schema = {
            "company_name": "string",
            "cin": "string",
            "meeting_details": {
                "date": "string",
                "time": "string",
                "location": "string"
            },
            "resolution_type": "string",
            "agenda_item_number": "string",
            "agenda_title": "string",
            "resolution_text": "string",
            "proposer": {
                "name": "string",
                "designation": "string"
            },
            "seconder": {
                "name": "string",
                "designation": "string"
            },
            "approval_result": "string",
            "directors_present": "string",
            "authorized_signatory": {
                "name": "string",
                "signature": "string"
            },
            "company_seal": "string",
            "certification_by": {
                "company_secretary": "string",
                "signature": "string"
            },
            "effective_date": "string"
        }
        return self._extract(text, schema, "Extract all fields related to Board Resolutions.")
