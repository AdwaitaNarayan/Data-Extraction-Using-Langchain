import logging
from typing import Optional
from schemas.bank_schema import BankSchema
from extraction.extractor_utils import OllamaExtractionUtils

logger = logging.getLogger(__name__)


class BankExtractor:
    """Bank statement extractor using standard fields"""

    def __init__(self):
        self.utils = OllamaExtractionUtils()

    def extract(self, text: str) -> Optional[BankSchema]:
        """Extract bank statement data matching your schema exactly"""

        additional_instructions = """
BANK STATEMENT EXTRACTION GUIDELINES:
- Extract account information: account_number, account_holder_name, bank_name
- Get statement period: statement_period_start, statement_period_end
- Find balances: opening_balance, closing_balance
- Parse all transactions with: transaction_date, description, reference_number, debit_amount, credit_amount, balance
- Distinguish between debit and credit amounts carefully
- Extract transaction types and references

IMPORTANT:
- Dates in DD-MM-YYYY format
- Numbers without currency symbols or commas
- Transactions should be in chronological order
- Use exact field names from schema
"""

        try:
            result = self.utils.extract_with_retry(
                text=text,
                schema=BankSchema,
                document_type="bank_statement",
                additional_instructions=additional_instructions
            )

            if result:
                result = self._post_process_bank_statement(result)
                logger.info("Bank statement extraction completed successfully")
                return result
            else:
                logger.error("Bank statement extraction failed")
                return None

        except Exception as e:
            logger.error(f"Bank statement extraction error: {str(e)}")
            return None

    def _post_process_bank_statement(self, bank_stmt: BankSchema) -> BankSchema:
        """Post-process extracted bank statement data"""

        # Normalize dates
        if bank_stmt.statement_period_start:
            bank_stmt.statement_period_start = self._normalize_date(bank_stmt.statement_period_start)
        if bank_stmt.statement_period_end:
            bank_stmt.statement_period_end = self._normalize_date(bank_stmt.statement_period_end)

        # Clean balance amounts
        bank_stmt.opening_balance = self._safe_float_conversion(bank_stmt.opening_balance)
        bank_stmt.closing_balance = self._safe_float_conversion(bank_stmt.closing_balance)

        # Process transactions
        if bank_stmt.transactions:
            for transaction in bank_stmt.transactions:
                transaction.transaction_date = self._normalize_date(transaction.transaction_date)
                transaction.debit_amount = self._safe_float_conversion(transaction.debit_amount)
                transaction.credit_amount = self._safe_float_conversion(transaction.credit_amount)
                transaction.balance = self._safe_float_conversion(transaction.balance)

        bank_stmt.document_type = "bank_statement"
        return bank_stmt

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
