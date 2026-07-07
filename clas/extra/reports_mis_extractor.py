from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser
import json

class ReportsMISExtractor:
    def __init__(self, model="llama2:latest", base_url="http://localhost:11434"):
        self.llm = ChatOllama(model=model, base_url=base_url)
        self.parser = JsonOutputParser()

    def _extract(self, text: str, schema: dict, doc_name: str):
        prompt = f"""
        You are a strict document information extractor.
        Extract ONLY the following fields from a {doc_name} document into valid JSON:

        {json.dumps(schema, indent=2)}

        Document:
        {text}
        """
        response = self.llm.invoke(prompt)
        return self.parser.parse(response.content)

    # 1️⃣ Trial Balance
    def extract_trial_balance(self, text: str):
        schema = {
            "report_date_or_period": "string",
            "company_name": "string",
            "financial_year": "string",
            "accounts": [
                {
                    "account_code": "string",
                    "account_name": "string",
                    "description": "string",
                    "debit_balance": "number",
                    "credit_balance": "number",
                }
            ],
            "total_debit": "number",
            "total_credit": "number",
            "prepared_by": "string",
            "verified_by": "string"
        }
        return self._extract(text, schema, "Trial Balance")

    # 2️⃣ Bank Reconciliation Statement
    def extract_bank_reconciliation_statement(self, text: str):
        schema = {
            "company_name": "string",
            "account_number": "string",
            "bank_name": "string",
            "branch": "string",
            "statement_period_start": "string",
            "statement_period_end": "string",
            "balance_as_per_bank": "number",
            "balance_as_per_books": "number",
            "deposits_in_transit": "number",
            "outstanding_cheques": "number",
            "bank_charges": "number",
            "interest": "number",
            "adjusted_balance": "number",
            "remarks": "string",
            "prepared_by": "string",
            "approved_by": "string"
        }
        return self._extract(text, schema, "Bank Reconciliation Statement")

    # 3️⃣ Inventory Valuation Report
    def extract_inventory_valuation_report(self, text: str):
        schema = {
            "report_period": "string",
            "inventory_items": [
                {
                    "item_code": "string",
                    "item_name": "string",
                    "batch_number": "string",
                    "opening_quantity": "number",
                    "opening_value": "number",
                    "purchases": "number",
                    "issues_or_sales": "number",
                    "closing_quantity": "number",
                    "unit_rate": "number",
                    "closing_value": "number",
                    "warehouse": "string",
                    "valuation_method": "string"
                }
            ],
            "total_inventory_value": "number"
        }
        return self._extract(text, schema, "Inventory Valuation Report")

    # 4️⃣ Fixed Asset Register
    def extract_fixed_asset_register(self, text: str):
        schema = {
            "assets": [
                {
                    "asset_id": "string",
                    "asset_name": "string",
                    "category": "string",
                    "purchase_date": "string",
                    "purchase_cost": "number",
                    "vendor_name": "string",
                    "invoice_number": "string",
                    "location": "string",
                    "useful_life_years": "number",
                    "depreciation_rate": "number",
                    "accumulated_depreciation": "number",
                    "net_book_value": "number",
                    "disposal_date": "string",
                    "disposal_proceeds": "number",
                    "custodian": "string"
                }
            ]
        }
        return self._extract(text, schema, "Fixed Asset Register")

    # 5️⃣ Accounts Aging Report
    def extract_accounts_aging_report(self, text: str):
        schema = {
            "report_date": "string",
            "party_type": "string",
            "entries": [
                {
                    "party_name": "string",
                    "party_code": "string",
                    "invoice_number": "string",
                    "invoice_date": "string",
                    "due_date": "string",
                    "total_amount": "number",
                    "outstanding_amount": "number",
                    "aging_days": "number",
                    "contact_info": "string",
                    "collector_name": "string",
                    "notes": "string"
                }
            ]
        }
        return self._extract(text, schema, "Accounts Aging Report")

    # 6️⃣ Budget Report
    def extract_budget_report(self, text: str):
        schema = {
            "department": "string",
            "period": "string",
            "accounts": [
                {
                    "account_code": "string",
                    "account_name": "string",
                    "budgeted_amount": "number",
                    "actual_amount": "number",
                    "variance_amount": "number",
                    "variance_percentage": "number",
                    "variance_reason": "string"
                }
            ],
            "approved_version_date": "string",
            "prepared_by": "string",
            "reviewed_by": "string"
        }
        return self._extract(text, schema, "Budget Report")

    # 7️⃣ Cost Sheet
    def extract_cost_sheet(self, text: str):
        schema = {
            "product_or_service_name": "string",
            "period": "string",
            "direct_materials": "number",
            "direct_labour": "number",
            "direct_expenses": "number",
            "factory_overheads": "number",
            "administrative_overheads": "number",
            "selling_overheads": "number",
            "total_cost_of_production": "number",
            "profit_margin_percentage": "number",
            "cost_per_unit": "number"
        }
        return self._extract(text, schema, "Cost Sheet")

    # 8️⃣ Forecasting Statement
    def extract_forecasting_statement(self, text: str):
        schema = {
            "forecast_period": "string",
            "account_category": "string",
            "method_used": "string",
            "historical_reference": "string",
            "predicted_values": "object",
            "key_assumptions": "string",
            "variance_from_previous": "number",
            "prepared_by": "string",
            "validation_status": "string"
        }
        return self._extract(text, schema, "Forecasting Statement")

    # 9️⃣ MIS Report
    def extract_mis_report(self, text: str):
        schema = {
            "reporting_period": "string",
            "department": "string",
            "kpis": [{"name": "string", "value": "number"}],
            "revenue_summary": {"actual": "number", "budget": "number"},
            "expense_breakdown": "object",
            "profitability_metrics": {"gross_margin": "number", "EBITDA": "number", "net_profit": "number"},
            "operational_ratios": {"inventory_turnover": "number", "DSO": "number", "DPO": "number"},
            "commentary": "string"
        }
        return self._extract(text, schema, "MIS Report")

    # 🔟 Performance Dashboard
    def extract_performance_dashboard(self, text: str):
        schema = {
            "dashboard_period": "string",
            "business_unit": "string",
            "kpis": [
                {
                    "name": "string",
                    "target": "number",
                    "actual": "number",
                    "variance": "number",
                    "status": "string"
                }
            ],
            "trend_data": "object",
            "notes": "string"
        }
        return self._extract(text, schema, "Performance Dashboard")
