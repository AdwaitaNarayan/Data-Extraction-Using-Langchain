from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Address(BaseModel):
    """Reusable address structure"""
    street: Optional[str] = Field(default=None, description="Street address")
    city: Optional[str] = Field(default=None, description="City name")
    state: Optional[str] = Field(default=None, description="State or province")
    pincode: Optional[str] = Field(default=None, description="Postal/ZIP code")
    country: Optional[str] = Field(default=None, description="Country name")


class BaseDocumentSchema(BaseModel):
    """Base schema with common fields for all documents"""

    document_type: Optional[str] = Field(default=None, description="Type of the document (invoice, payroll, etc.)")
    source_file: Optional[str] = Field(default=None, description="Original file name of the document")
    extraction_date: Optional[str] = Field(
        default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        description="Timestamp when extraction was performed"
    )
