from typing import Optional
from pydantic import Field
from schemas.base_schema import BaseDocumentSchema


class PayrollSchema(BaseDocumentSchema):
    # Employee Information
    employee_id: Optional[str] = Field(default=None, description="Employee ID")
    employee_name: Optional[str] = Field(default=None, description="Employee name")
    department: Optional[str] = Field(default=None, description="Department")
    designation: Optional[str] = Field(default=None, description="Job designation")

    # Salary Information
    gross_salary: Optional[float] = Field(default=None, description="Gross salary amount")
    net_salary: Optional[float] = Field(default=None, description="Net salary amount")
    basic_salary: Optional[float] = Field(default=None, description="Basic salary amount")

    # Allowances
    da_allowance: Optional[float] = Field(default=None, description="Dearness Allowance")
    hra_allowance: Optional[float] = Field(default=None, description="House Rent Allowance")
    conveyance_allowance: Optional[float] = Field(default=None, description="Conveyance allowance")
    medical_allowance: Optional[float] = Field(default=None, description="Medical allowance")
    other_allowances: Optional[float] = Field(default=None, description="Other allowances")

    # Deductions
    pf_deduction: Optional[float] = Field(default=None, description="Provident Fund deduction")
    esi_deduction: Optional[float] = Field(default=None, description="ESI deduction")
    income_tax: Optional[float] = Field(default=None, description="Income tax deduction")
    professional_tax: Optional[float] = Field(default=None, description="Professional tax")
    other_deductions: Optional[float] = Field(default=None, description="Other deductions")

    # Pay Period
    pay_period_start: Optional[str] = Field(default=None, description="Pay period start date (DD-MM-YYYY)")
    pay_period_end: Optional[str] = Field(default=None, description="Pay period end date (DD-MM-YYYY)")

    # Bank Details
    bank_name: Optional[str] = Field(default=None, description="Bank name")
    account_number: Optional[str] = Field(default=None, description="Bank account number")
    ifsc_code: Optional[str] = Field(default=None, description="IFSC code")
