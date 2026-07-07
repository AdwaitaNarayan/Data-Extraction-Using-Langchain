from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.base_schema import BaseDocumentSchema


class BankTransaction(BaseModel):
    transaction_date: Optional[str] = Field(None, description="Transaction date")
    description: Optional[str] = Field(None, description="Transaction description")
    reference_number: Optional[str] = Field(None, description="Reference number")
    debit_amount: Optional[float] = Field(None, description="Debit amount")
    credit_amount: Optional[float] = Field(None, description="Credit amount")
    balance: Optional[float] = Field(None, description="Balance after transaction")


class BankSchema(BaseDocumentSchema):
    # Account information
    account_number: Optional[str] = Field(None, description="Bank account number")
    account_holder_name: Optional[str] = Field(None, description="Account holder name")
    bank_name: Optional[str] = Field(None, description="Bank name")

    # Statement period
    statement_period_start: Optional[str] = Field(None, description="Statement start date")
    statement_period_end: Optional[str] = Field(None, description="Statement end date")

    # Balances
    opening_balance: Optional[float] = Field(None, description="Opening balance")
    closing_balance: Optional[float] = Field(None, description="Closing balance")

    # Transactions
    transactions: List[BankTransaction] = Field(default_factory=list, description="List of transactions")
