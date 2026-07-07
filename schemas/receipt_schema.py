from typing import Optional
from pydantic import Field
from schemas.base_schema import BaseDocumentSchema, Address


class ReceiptSchema(BaseDocumentSchema):
    # Basic Information
    receipt_number: Optional[str] = Field(default=None, description="Receipt number")
    receipt_date: Optional[str] = Field(default=None, description="Receipt date (DD-MM-YYYY)")

    # Party Information
    party_name: Optional[str] = Field(default=None, description="Payer name")
    party_address: Optional[Address] = Field(default=None, description="Payer address")

    # Payment Details
    amount_paid: Optional[float] = Field(default=None, description="Amount paid")
    payment_method: Optional[str] = Field(default=None, description="Payment method")

    # Bank Details
    bank_details: Optional[str] = Field(default=None, description="Bank details")
    cheque_number: Optional[str] = Field(default=None, description="Cheque number")
    transaction_id: Optional[str] = Field(default=None, description="Transaction ID")

    # Financial Details
    subtotal: Optional[float] = Field(default=None, description="Subtotal amount")
    tax_amount: Optional[float] = Field(default=None, description="Tax amount")
    total_amount: Optional[float] = Field(default=None, description="Total amount")

    # Additional Information
    company_name: Optional[str] = Field(default=None, description="Company name")
    reference_number: Optional[str] = Field(default=None, description="Reference number")
    invoice_number: Optional[str] = Field(default=None, description="Related invoice number")
    status: Optional[str] = Field(default=None, description="Receipt status")
    remarks: Optional[str] = Field(default=None, description="Additional remarks")
