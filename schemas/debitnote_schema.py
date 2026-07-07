from typing import Optional
from pydantic import BaseModel, Field
from schemas.base_schema import BaseDocumentSchema, Address


class DebitNoteSchema(BaseDocumentSchema):
    # Note identification
    debit_note_number: Optional[str] = Field(default=None, description="Debit note number")
    debit_date: Optional[str] = Field(default=None, description="Debit date")

    # Party information
    vendor_name: Optional[str] = Field(default=None, description="Vendor name")
    vendor_address: Optional[str] = Field(default=None, description="Vendor address")

    # Reference information
    linked_invoice_id: Optional[str] = Field(default=None, description="Linked invoice ID")

    # Financial details
    debit_amount: Optional[float] = Field(default=None, description="Debit amount")
    cgst_amount: Optional[float] = Field(default=None, description="CGST amount")
    sgst_amount: Optional[float] = Field(default=None, description="SGST amount")
    igst_amount: Optional[float] = Field(default=None, description="IGST amount")

    # Additional details
    reason: Optional[str] = Field(default=None, description="Reason for debit note")
    reference_number: Optional[str] = Field(default=None, description="Reference number")
    status: Optional[str] = Field(default=None, description="Status")
    company_name: Optional[str] = Field(default=None, description="Company name")
