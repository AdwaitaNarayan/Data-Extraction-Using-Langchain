from typing import List, Optional
from pydantic import BaseModel, Field
from schemas.base_schema import BaseDocumentSchema, Address


class InvoiceItem(BaseModel):
    product_name: Optional[str] = Field(default=None, description="Product/item name")
    manufacturer_name: Optional[str] = Field(default=None, description="Manufacturer name")
    batch_number: Optional[str] = Field(default=None, description="Batch number")
    hsn_code: Optional[str] = Field(default=None, description="HSN/SAC code")
    quantity: Optional[float] = Field(default=None, description="Quantity")
    mrp: Optional[float] = Field(default=None, description="MRP/unit price")
    discount_percent: Optional[float] = Field(default=None, description="Discount percentage")
    taxable_amount: Optional[float] = Field(default=None, description="Taxable amount")
    cgst_rate: Optional[float] = Field(default=None, description="CGST rate")
    cgst_amount: Optional[float] = Field(default=None, description="CGST amount")
    sgst_rate: Optional[float] = Field(default=None, description="SGST rate")
    sgst_amount: Optional[float] = Field(default=None, description="SGST amount")
    igst_rate: Optional[float] = Field(default=None, description="IGST rate")
    igst_amount: Optional[float] = Field(default=None, description="IGST amount")


class InvoiceDescription(BaseModel):
    section: Optional[str] = Field(default=None, description="Description section")
    text: Optional[str] = Field(default=None, description="Description text")
    page: Optional[int] = Field(default=None, description="Page number")
    amount: Optional[float] = Field(default=None, description="Associated amount")


class InvoiceSchema(BaseDocumentSchema):
    # Basic Information
    invoice_number: Optional[str] = Field(default=None, description="Invoice number")
    invoice_date: Optional[str] = Field(default=None, description="Invoice date (DD-MM-YYYY)")
    due_date: Optional[str] = Field(default=None, description="Payment due date (DD-MM-YYYY)")

    # Party Details
    party_name: Optional[str] = Field(default=None, description="Customer/vendor name")
    party_type: Optional[str] = Field(default=None, description="Party type (customer/vendor)")
    party_gstin: Optional[str] = Field(default=None, description="Party GSTIN")
    party_address: Optional[Address] = Field(default=None, description="Party address")
    party_email: Optional[str] = Field(default=None, description="Party email")
    party_phone: Optional[str] = Field(default=None, description="Party phone")

    # Financial Details
    base_amount: Optional[float] = Field(default=None, description="Base taxable amount")
    cgst_rate: Optional[float] = Field(default=None, description="CGST rate percentage")
    cgst_amount: Optional[float] = Field(default=None, description="CGST amount")
    sgst_rate: Optional[float] = Field(default=None, description="SGST rate percentage")
    sgst_amount: Optional[float] = Field(default=None, description="SGST amount")
    igst_rate: Optional[float] = Field(default=None, description="IGST rate percentage")
    igst_amount: Optional[float] = Field(default=None, description="IGST amount")
    total_amount: Optional[float] = Field(default=None, description="Total invoice amount")

    # Accounting Information
    debit_account: Optional[str] = Field(default=None, description="Debit account")
    credit_account: Optional[str] = Field(default=None, description="Credit account")
    description: Optional[str] = Field(default=None, description="Invoice description")

    # Additional Fields
    reference_number: Optional[str] = Field(default=None, description="Reference number")
    status: Optional[str] = Field(default=None, description="Invoice status")
    company_name: Optional[str] = Field(default=None, description="Company name")
    invoice_type: Optional[str] = Field(default=None, description="Invoice type")
    hsn_code: Optional[str] = Field(default=None, description="HSN/SAC code")

    # Complex Structures
    invoice_items: Optional[List[InvoiceItem]] = Field(default=None, description="List of invoice items")
    descriptions: Optional[List[InvoiceDescription]] = Field(default=None, description="Invoice descriptions")
