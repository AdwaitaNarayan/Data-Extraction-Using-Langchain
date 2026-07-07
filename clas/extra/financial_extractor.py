from langchain_ollama import ChatOllama
from langchain_core.output_parsers.json import JsonOutputParser
import json


class FinancialExtractor:
    """
    Extractor for financial statements:
      - Balance Sheet
      - Income Statement
      - Cash Flow Statement
      - Statement of Changes in Equity
      - Notes to Accounts
    """

    def __init__(self, model="llama2:latest", base_url="http://localhost:11434"):
        self.llm = ChatOllama(model=model, base_url=base_url)
        self.parser = JsonOutputParser()

    def _extract(self, text: str, schema: dict, instruction: str) -> dict:
        """Generic extractor utility"""
        prompt = f"""
        You are an expert financial document data extractor.
        Extract ONLY the following fields in valid JSON format.
        Use the provided schema as guidance.

        Schema:
        {json.dumps(schema, indent=2)}

        Rules:
        - Match all numeric and textual values exactly.
        - Return null if a field is not available.
        - Preserve structure and hierarchy.

        {instruction}

        Document:
        {text}
        """
        response = self.llm.invoke(prompt)
        return self.parser.parse(response.content)

    # --------------------------------------------------------------------------
    def extract_balance_sheet(self, text: str):
        schema = {
            "date_of_statement": "string",
            "company_name": "string",
            "fiscal_year": "string",
            "currency": "string",
            "assets": {
                "current_assets": {
                    "cash_and_cash_equivalents": "number",
                    "marketable_securities": "number",
                    "accounts_receivable": "number",
                    "inventory": "number",
                    "prepaid_expenses": "number",
                    "other_current_assets": "number"
                },
                "non_current_assets": {
                    "property_plant_equipment": "number",
                    "accumulated_depreciation": "number",
                    "intangible_assets": "number",
                    "long_term_investments": "number",
                    "deferred_tax_assets": "number"
                }
            },
            "liabilities": {
                "current_liabilities": {
                    "accounts_payable": "number",
                    "accrued_expenses": "number",
                    "short_term_loans": "number",
                    "income_tax_payable": "number",
                    "other_current_liabilities": "number"
                },
                "non_current_liabilities": {
                    "long_term_borrowings": "number",
                    "lease_obligations": "number",
                    "deferred_tax_liabilities": "number",
                    "provisions_and_pensions": "number"
                }
            },
            "equity": {
                "share_capital": "number",
                "additional_paid_in_capital": "number",
                "retained_earnings": "number",
                "treasury_shares": "number",
                "reserves": "number",
                "total_equity": "number"
            },
            "totals": {
                "total_assets": "number",
                "total_liabilities": "number",
                "total_equity": "number",
                "balancing_check": "string"
            }
        }
        return self._extract(text, schema, "Extract all fields for a Balance Sheet document.")

    # --------------------------------------------------------------------------
    def extract_income_statement(self, text: str):
        schema = {
            "period_from": "string",
            "period_to": "string",
            "company_name": "string",
            "fiscal_year": "string",
            "revenue": {
                "gross_revenue": "number",
                "returns_and_allowances": "number",
                "net_revenue": "number"
            },
            "expenses": {
                "cost_of_goods_sold": "number",
                "selling_expenses": "number",
                "administrative_expenses": "number",
                "marketing_expenses": "number",
                "depreciation_amortization": "number"
            },
            "profit_loss": {
                "gross_profit": "number",
                "operating_income": "number",
                "other_income": {
                    "interest_income": "number",
                    "dividend_income": "number",
                    "gains_on_investments": "number"
                },
                "other_expenses": {
                    "interest_expense": "number",
                    "losses_on_investments": "number"
                },
                "profit_before_tax": "number",
                "income_tax_expense": "number",
                "net_income": "number",
                "other_comprehensive_income": "number",
                "total_comprehensive_income": "number",
                "earnings_per_share": "number"
            }
        }
        return self._extract(text, schema, "Extract all fields for an Income Statement document.")

    # --------------------------------------------------------------------------
    def extract_cash_flow_statement(self, text: str):
        schema = {
            "period_from": "string",
            "period_to": "string",
            "currency": "string",
            "net_income": "number",
            "non_cash_adjustments": {
                "depreciation": "number",
                "amortization": "number"
            },
            "changes_in_working_capital": {
                "accounts_receivable": "number",
                "inventory": "number",
                "accounts_payable": "number",
                "other_adjustments": "number"
            },
            "cash_from_operating_activities": "number",
            "cash_from_investing_activities": {
                "purchase_or_sale_of_assets": "number",
                "investments_made": "number",
                "loans_issued_or_collected": "number"
            },
            "cash_from_financing_activities": {
                "share_issuance_or_repurchase": "number",
                "borrowings_proceeds_or_repayments": "number",
                "dividend_payments": "number"
            },
            "net_change_in_cash": "number",
            "opening_cash_balance": "number",
            "closing_cash_balance": "number",
            "supplementary_disclosures": {
                "interest_paid": "number",
                "income_tax_paid": "number"
            }
        }
        return self._extract(text, schema, "Extract all fields for a Cash Flow Statement document.")

    # --------------------------------------------------------------------------
    def extract_statement_of_changes_in_equity(self, text: str):
        schema = {
            "share_capital": {
                "opening_balance": "number",
                "changes": "number",
                "closing_balance": "number"
            },
            "reserves": {
                "opening_balance": "number",
                "transfers": "number",
                "closing_balance": "number"
            },
            "retained_earnings": {
                "opening_balance": "number",
                "net_income": "number",
                "dividends": "number",
                "closing_balance": "number"
            },
            "other_comprehensive_income": "number",
            "total_equity_end_of_period": "number",
            "adjustments": {
                "policy_changes": "string",
                "share_buybacks": "number",
                "revaluation_surplus": "number"
            }
        }
        return self._extract(text, schema, "Extract all fields for a Statement of Changes in Equity document.")

    # --------------------------------------------------------------------------
    def extract_notes_to_accounts(self, text: str):
        schema = {
            "accounting_policies": "string",
            "basis_of_preparation": "string",
            "changes_in_estimates": "string",
            "contingent_liabilities": "string",
            "commitments_and_guarantees": "string",
            "related_party_transactions": "string",
            "segment_reporting": "string",
            "employee_benefit_plans": "string",
            "tax_reconciliation": "string",
            "ppe_schedule": "string",
            "revenue_recognition": "string",
            "financial_risk_management": "string",
            "events_after_reporting_date": "string",
            "auditor_notes": "string"
        }
        return self._extract(text, schema, "Extract all fields for Notes to Accounts.")
