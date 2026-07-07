from clas.extra.financial_extractor import FinancialExtractor
from clas.extra.invoices_vouchers_extractor import InvoicesVouchersExtractor
from clas.extra.journals_ledgers_extractor import JournalsLedgersExtractor
from clas.extra.reports_mis_extractor import ReportsMISExtractor
from clas.extra.tax_compliance_extractor import TaxComplianceExtractor


def get_extractor(document_type: str):
    """Return appropriate extractor instance & method for a given document type."""
    mapping = {
        # ---------------- Invoices & Vouchers ----------------
        "Sales Invoice": (InvoicesVouchersExtractor, "extract_sales_invoice"),
        "Purchase Invoice": (InvoicesVouchersExtractor, "extract_purchase_invoice"),
        "Receipt": (InvoicesVouchersExtractor, "extract_receipt"),
        "Payment Voucher": (InvoicesVouchersExtractor, "extract_payment_voucher"),
        "Bank Statement": (InvoicesVouchersExtractor, "extract_bank_statement"),
        "Payroll": (InvoicesVouchersExtractor, "extract_payroll"),
        "Expense Voucher": (InvoicesVouchersExtractor, "extract_expense_voucher"),
        "Credit Note": (InvoicesVouchersExtractor, "extract_credit_note"),
        "Debit Note": (InvoicesVouchersExtractor, "extract_debit_note"),

        # ---------------- Financial Statements ----------------
        "Balance Sheet": (FinancialExtractor, "extract_balance_sheet"),
        "Income Statement": (FinancialExtractor, "extract_income_statement"),
        "Cash Flow Statement": (FinancialExtractor, "extract_cash_flow_statement"),
        "Statement of Changes in Equity": (FinancialExtractor, "extract_statement_of_changes_in_equity"),
        "Notes to Accounts": (FinancialExtractor, "extract_notes_to_accounts"),

        # ---------------- Journals & Ledgers ----------------
        "General Journal": (JournalsLedgersExtractor, "extract_general_journal"),
        "General Ledger": (JournalsLedgersExtractor, "extract_general_ledger"),
        "Cash Book": (JournalsLedgersExtractor, "extract_cash_book"),
        "Petty Cash Book": (JournalsLedgersExtractor, "extract_petty_cash_book"),
        "Accounts Payable Ledger": (JournalsLedgersExtractor, "extract_accounts_payable_ledger"),
        "Accounts Receivable Ledger": (JournalsLedgersExtractor, "extract_accounts_receivable_ledger"),

        # ---------------- Reports & MIS ----------------
        "Trial Balance": (ReportsMISExtractor, "extract_trial_balance"),
        "Bank Reconciliation Statement": (ReportsMISExtractor, "extract_bank_reconciliation_statement"),
        "Inventory Valuation Report": (ReportsMISExtractor, "extract_inventory_valuation_report"),
        "Fixed Asset Register": (ReportsMISExtractor, "extract_fixed_asset_register"),
        "Accounts Aging Report": (ReportsMISExtractor, "extract_accounts_aging_report"),
        "Budget Report": (ReportsMISExtractor, "extract_budget_report"),
        "Cost Sheet": (ReportsMISExtractor, "extract_cost_sheet"),
        "Forecasting Statement": (ReportsMISExtractor, "extract_forecasting_statement"),
        "MIS Report": (ReportsMISExtractor, "extract_mis_report"),
        "Performance Dashboard": (ReportsMISExtractor, "extract_performance_dashboard"),

        # ---------------- Tax & Compliance ----------------
        "Tax Return": (TaxComplianceExtractor, "extract_tax_return"),
        "Audit Report": (TaxComplianceExtractor, "extract_audit_report"),
        "Annual Report": (TaxComplianceExtractor, "extract_annual_report"),
        "GST Compliance Reports": (TaxComplianceExtractor, "extract_gst_compliance_reports"),
        "Company Incorporation Docs": (TaxComplianceExtractor, "extract_company_incorporation_docs"),
        "Board Resolutions": (TaxComplianceExtractor, "extract_board_resolutions"),
    }

    if document_type not in mapping:
        raise ValueError(f"No extractor defined for {document_type}")

    cls, method_name = mapping[document_type]
    instance = cls()
    return getattr(instance, method_name)
