from typing import Optional
from pydantic import BaseModel, Field
from schemas.base_schema import BaseDocumentSchema, Address


class CreditNoteSchema(BaseDocumentSchema):
    # Note identification
    credit_note_number: Optional[str] = Field(default=None, description="Credit note number")
    credit_date: Optional[str] = Field(default=None, description="Credit date")

    # Party information
    customer_name: Optional[str] = Field(default=None, description="Customer name")
    customer_address: Optional[str] = Field(default=None, description="Customer address")

    # Financial details
    credit_amount: Optional[float] = Field(default=None, description="Credit amount")
    cgst_amount: Optional[float] = Field(default=None, description="CGST amount")
    sgst_amount: Optional[float] = Field(default=None, description="SGST amount")
    igst_amount: Optional[float] = Field(default=None, description="IGST amount")

    # Additional details
    reason: Optional[str] = Field(default=None, description="Reason for credit note")
    reference_number: Optional[str] = Field(default=None, description="Reference number")
    status: Optional[str] = Field(default=None, description="Status")
    company_name: Optional[str] = Field(default=None, description="Company name")
